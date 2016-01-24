from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from certificates.models import SSLRevokedCertificate
from celery.utils.log import get_task_logger
from  celery import shared_task
import datetime
import time
import pytz

logger = get_task_logger(__name__)

@shared_task(bind=True)
def regenerate_certificate_revocation_list(self, certification_authority):
    logger.info("Updating CRL for CA %s" % certification_authority.common_name)
    one_day = datetime.timedelta(1, 0, 0)
    ca_cert =  x509.load_pem_x509_certificate(str(certification_authority.certificate), default_backend())
    ca_key =  serialization.load_pem_private_key(str(certification_authority.private_key), None, default_backend())

    builder = x509.CertificateRevocationListBuilder()
    builder = builder.issuer_name(ca_cert.subject)
    builder = builder.last_update(datetime.datetime.today())
    builder = builder.next_update(datetime.datetime.today() + one_day)

    for certificate in SSLRevokedCertificate.objects.filter(certification_authority=certification_authority):
        logger.info("Adding certificate 0x%X" % certificate.serial_number)
        revoked_cert = x509.RevokedCertificateBuilder().serial_number(
            certificate.serial_number
        ).revocation_date(
            certificate.revocation_date.replace(tzinfo=None)
        ).build(default_backend())

        builder = builder.add_revoked_certificate(revoked_cert)
    crl = builder.sign(
        private_key=ca_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    logger.info('Saving models')
    certification_authority.revocation_list = crl.public_bytes(serialization.Encoding.PEM)
    print certification_authority.revocation_list
    certification_authority.save()
