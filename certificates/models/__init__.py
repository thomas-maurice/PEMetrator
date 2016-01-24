# -*- coding: utf-8 -*-

from certification_authority import SSLCertificationAuthority
from certificate import SSLCertificate
from certificate_request import SSLCertificateRequest
from revoked_certificate import SSLRevokedCertificate
from django.db.models import signals
from certificates.tasks import regenerate_certificate_revocation_list

def SSLCertificate_pre_delete(sender, instance, **kwargs):
    """Hook to ensure that a deleted certificate is proprely revoked"""
    instance.status = 'REVOKED'
    instance.save()
    if SSLRevokedCertificate.objects.filter(
        certification_authority=instance.certification_authority,
        serial_number=instance.serial_number).count() != 0:
            return
    revoked = SSLRevokedCertificate(
        certification_authority=instance.certification_authority,
        serial_number=instance.serial_number,
        reason="CESSATION_OF_OPERATION",
    )
    revoked.save()
    regenerate_certificate_revocation_list.delay(instance.certification_authority)
    instance.certificate_request.delete()

signals.pre_delete.connect(SSLCertificate_pre_delete, sender=SSLCertificate)