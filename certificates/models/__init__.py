# -*- coding: utf-8 -*-

from certification_authority import SSLCertificationAuthority
from certificate import SSLCertificate
from certificate_request import SSLCertificateRequest
from revoked_certificate import SSLRevokedCertificate
from django.db.models import signals
from certificates.tasks import regenerate_certificate_revocation_list
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def SSLCertificate_pre_delete(sender, instance, **kwargs):
    """Hook to ensure that a deleted certificate is proprely revoked"""
    if instance.status != 'REVOKED' and instance.status != "EXPIRED":
        logging.warn("Revoking certificate %s, serial 0x%x because it is to be deleted" % (
                instance.certificate_request.common_name,
                instance.serial_number
            )
        )
        instance.status = 'REVOKED'
        instance.save()
    if SSLRevokedCertificate.objects.filter(
        certification_authority=instance.certification_authority,
        serial_number=instance.serial_number).count() == 0:
            revoked = SSLRevokedCertificate(
                certification_authority=instance.certification_authority,
                serial_number=instance.serial_number,
                reason="CESSATION_OF_OPERATION",
            )
            revoked.save()
    logging.warn("Removing the corresponding certificate request %s" % instance.certificate_request.common_name)
    instance.certificate_request.delete()

signals.pre_delete.connect(SSLCertificate_pre_delete, sender=SSLCertificate)
