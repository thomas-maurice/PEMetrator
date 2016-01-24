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
from certificate import sign_certificate_request
import datetime
import pytz

utc=pytz.UTC
logger = get_task_logger(__name__)

@shared_task(bind=True)
def create_certificate_request(self, cert, rsa_password=None, auto_sign=True):
    logger.info('Initializing CSR %s' % cert.common_name)
    cert.status = 'GENERATING'
    cert.save()

    one_day = datetime.timedelta(1,0,0)

    logger.info("Generating %d bits long private key" % cert.private_key_size)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=cert.private_key_size,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    encryption_algorithm = serialization.NoEncryption()

    if rsa_password:
        encryption_algorithm = serialization.BestAvailableEncryption(bytes(rsa_password))

    cert.private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )

    logger.info("Building Certificate Signing Request, CN: %s" % cert.common_name)

    builder = x509.CertificateSigningRequestBuilder()

    name_attributes = [x509.NameAttribute(NameOID.COMMON_NAME, cert.common_name)]
    if cert.country_name:
        logger.debug('C: %s' % cert.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.COUNTRY_NAME, cert.country_name))
    if cert.locality_name:
        logger.debug('L: %s' % cert.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.LOCALITY_NAME, cert.locality_name))
    if cert.state_name:
        logger.debug('ST: %s' % cert.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, cert.state_name))
    if cert.organization_name:
        logger.debug('O: %s' % cert.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME, cert.organization_name))
    if cert.organization_unit_name:
        logger.debug('OU: %s' % cert.country_name)
        name_attributes.append(x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, cert.organization_unit_name))

    name = x509.Name(name_attributes)
    builder = builder.subject_name(name)
    builder = builder.add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True,
    )

    if cert.server_certificate:
        logger.info("Adding SSL Server informations to the certificate")
        builder = builder.add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=True,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False
            ), critical=True
        ).add_extension(
            x509.ExtendedKeyUsage(
                [x509.oid.ExtendedKeyUsageOID.SERVER_AUTH]
            ), critical=True
        )
    else:
        logger.info("Adding SSL Client informations to the certificate")
        builder = builder.add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=True,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False
            ), critical=True
        ).add_extension(
            x509.ExtendedKeyUsage(
                [x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH]
            ), critical=True
        )


    request = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    logger.info("Exporting certificate")
    cert.request = request.public_bytes(serialization.Encoding.PEM)

    logger.info('Saving model')
    cert.status = 'VALIDATING'
    cert.save()

    logger.info('Certificate signing request generation complete')
    send_mail(subject="Certificate signing request for %s" % cert.common_name,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[cert.user.email],
        message="""Your certificate signing request has been created.

The request is this one:

%s

The private key associated is the following:

%s
        """ % (cert.request, cert.private_key)
    )
    if auto_sign:
        sign_certificate_request.delay(cert)
