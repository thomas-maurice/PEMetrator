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
from django.db.models.signals import post_save
from django.conf import settings
from certification_authority import SSLCertificationAuthority

import pycountry

COUNTRIES = tuple()
for country in list(pycountry.countries):
    COUNTRIES += ((country.alpha2, country.name), )

class SSLCertificateRequest(models.Model):
    certification_authority = models.ForeignKey(
        SSLCertificationAuthority,
        on_delete=models.SET_NULL,
        help_text="The certification authority you want your certificate signed by",
        null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="User owning the certificate"
    )
    server_certificate = models.BooleanField(
        default=False,
        help_text="Is this certificate intended for a server instead of a client ?",
        blank=True,
    )
    common_name = models.CharField(
        max_length=255,
        help_text="Common Name of the certificate",
    )
    country_name = models.CharField(
        max_length=255,
        help_text="Country Name of the certificate",
        choices=COUNTRIES,
        default="FR",
        blank=True,
    )
    locality_name = models.CharField(
        max_length=255,
        help_text="Locality of the certificate",
        default="",
        blank=True,
    )
    state_name = models.CharField(
        max_length=255,
        help_text="State or province name of the certificate",
        default="",
        blank=True,
    )
    organization_name = models.CharField(
        max_length=255,
        help_text="Organization name of the certificate",
        default="",
        blank=True,
    )
    organization_unit_name = models.CharField(
        max_length=255,
        help_text="Organization unit name of the certificate",
        default="",
        blank=True,
    )
    private_key = models.TextField(
        help_text="Private key of the certificate",
        default="",
        blank=True,
        editable=False,
    )
    private_key_size = models.IntegerField(
        help_text="Size of the private key",
        choices=(
            (1024, '1024 bits'),
            (2048, '2048 bits'),
            (4096, '4096 bits'),
        ),
        default=4096,
    )
    request = models.TextField(
        help_text="Certificate Signing Request",
        default="",
        blank=True,
    )
    status = models.CharField(
        max_length=32,
        choices=(
            ('GENERATING', 'Generating'),
            ('VALIDATING', 'Waiting to be signed'),
            ('DECLINED', 'The certificate request was declined'),
            ('SIGNING', 'Signing'),
            ('SIGNED', 'Signed'),
            ('FAILED', 'Failed to be signed'),
        ),
        default="GENERATING",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.common_name

    class Meta:
        verbose_name = "SSL certificate request"
        verbose_name_plural = "SSL certificate requests"
