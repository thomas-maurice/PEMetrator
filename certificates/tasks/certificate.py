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
from certificates.models import SSLCertificate
import datetime
import pytz

utc=pytz.UTC
logger = get_task_logger(__name__)

@shared_task(bind=True)
def sign_certificate_request(self, csr):
    if csr.status != 'VALIDATING' and csr.status != 'FAILED':
        raise Exception("Certificate could not be validated, in %s state instead of VALIDATING or FAILED" % csr.status)
    one_day = datetime.timedelta(1,0,0)
    logger.info('Signing CSR %s' % csr.common_name)
    csr.status = 'SIGNING'
    csr.save()

    request = x509.load_pem_x509_csr(str(csr.request), default_backend())
    ca_cert =  x509.load_pem_x509_certificate(str(csr.certification_authority.certificate), default_backend())
    ca_key =  serialization.load_pem_private_key(str(csr.certification_authority.private_key), None, default_backend())
    builder = x509.CertificateBuilder()

    name = x509.Name(request.subject)
    builder = builder.subject_name(name)
    builder = builder.issuer_name(ca_cert.subject)
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime.today() + datetime.timedelta(days=365))
    builder = builder.serial_number(csr.id)
    builder = builder.public_key(request.public_key())
    for extension in request.extensions:
        builder = builder.add_extension(extension.value, critical=extension.critical)
    certificate = builder.sign(
        private_key=ca_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    logger.info("Exporting certificate")
    signed_cert_str = certificate.public_bytes(serialization.Encoding.PEM)
    logger.info('Saving model')
    signed_cert = SSLCertificate(
        certificate_request = csr,
        serial_number = csr.id,
        certification_authority=csr.certification_authority,
        certificate = signed_cert_str,
        expires_at = datetime.datetime.today() + datetime.timedelta(days=365),
        status = "VALID"
    )
    signed_cert.save()
    csr.status = "SIGNED"
    csr.save()
    logger.info('Certificate signing complete')
    send_mail(subject="Certificate for %s" % csr.common_name,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[csr.user.email],
        message="""Your certificate has been signed.

The certificate is this one:

%s""" % (signed_cert.certificate)
    )
