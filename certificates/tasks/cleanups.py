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

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from certificates.models import SSLCertificate
from django.utils import timezone
import pytz

logger = get_task_logger(__name__)

@shared_task(bind=True)
def check_expired_certificates(self):
    logger.info('Warning checking for expired certificates')
    expired = SSLCertificate.objects.filter(
        ~Q(status="EXPIRED") & Q(expires_at__lt=timezone.now())
    )
    for certificate in expired:
        logger.warn(
            "Marking certificate %s, serial 0x%x as expired" % (
                certificate.certificate_request.common_name,
                certificate.serial_number
            )
        )
        certificate.status = "EXPIRED"
        certificate.save()
