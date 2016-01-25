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

from django.db import models
from django.utils import timezone
from django.conf import settings
from certification_authority import SSLCertificationAuthority
from certificate_request import SSLCertificateRequest

import pycountry

COUNTRIES = tuple()
for country in list(pycountry.countries):
    COUNTRIES += ((country.alpha2, country.name), )

class SSLCertificate(models.Model):
    certificate_request = models.OneToOneField(
        SSLCertificateRequest,
        help_text="The corresponding request",
        related_name='signed_certificate',
        on_delete=models.CASCADE,
        null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User owning the certificate"
    )
    certification_authority = models.ForeignKey(
        SSLCertificationAuthority,
        on_delete=models.CASCADE,
        help_text="The certification authority that signed the certificate"
    )
    serial_number = models.IntegerField(
        help_text="Serial number of the certificate"
    )
    certificate = models.TextField(
        help_text="Certificate",
        default="",
        blank=True,
    )
    status = models.CharField(
        max_length=32,
        choices=(
            ('CREATING', 'Creating'),
            ('VALID', 'Valid'),
            ('REVOKED', 'Revoked'),
            ('EXPIRED', 'Expired')
        ),
        default="CREATING",
        blank=True,
    )

    expires_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.certificate_request.common_name

    class Meta:
        verbose_name = "SSL certificate"
        verbose_name_plural = "SSL certificates"
