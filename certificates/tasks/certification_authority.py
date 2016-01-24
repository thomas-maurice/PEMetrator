# -*- coding: utf-8 -*-

# Copyright (C) 2015 Thomas Maurice <thomas@maurice.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.conf import settings
import datetime
import pytz

from certificate_revocation import regenerate_certificate_revocation_list

utc=pytz.UTC
logger = get_task_logger(__name__)

@shared_task(bind=True)
def initialize_certification_authority(self, ca):
    logger.info('Initializing CA %s' % ca.common_name)
    ca.status = 'GENERATING'
    ca.save()

    one_day = datetime.timedelta(1,0,0)

    logger.info("Generating %d bits long private key" % ca.private_key_size)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=ca.private_key_size,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    ca.private_key=private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    logger.info("Building certificate, CN: %s" % ca.common_name)

    builder = x509.CertificateBuilder()

    name_attributes = [x509.NameAttribute(NameOID.COMMON_NAME, ca.common_name)]
    if ca.country_name:
        logger.debug('C: %s' % ca.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.COUNTRY_NAME, ca.country_name))
    if ca.locality_name:
        logger.debug('L: %s' % ca.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.LOCALITY_NAME, ca.locality_name))
    if ca.state_name:
        logger.debug('ST: %s' % ca.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, ca.state_name))
    if ca.organization_name:
        logger.debug('O: %s' % ca.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME, ca.organization_name))
    if ca.organization_unit_name:
        logger.debug('OU: %s' % ca.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, ca.organization_unit_name))

    name = x509.Name(name_attributes)
    builder = builder.subject_name(name)
    builder = builder.issuer_name(name)
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(ca.expires_at.replace(tzinfo=None))
    builder = builder.serial_number(1)
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    ).add_extension(
        x509.KeyUsage(
            digital_signature=False,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=True,
            crl_sign=True,
            encipher_only=False,
            decipher_only=False
        ), critical=False,
    ).add_extension(
        x509.SubjectKeyIdentifier.from_public_key(public_key), critical=False
    ).add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(public_key), critical=False
    )
    certificate = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    logger.info("Exporting certificate")
    ca.certificate = certificate.public_bytes(serialization.Encoding.PEM)
    logger.info('Saving model')
    ca.status = 'VALID'
    ca.save()
    logger.info('CA generation complete')
    regenerate_certificate_revocation_list.delay(ca)
