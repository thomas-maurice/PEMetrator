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
from django.conf import settings

import pycountry

COUNTRIES = tuple()
for country in list(pycountry.countries):
    COUNTRIES += ((country.alpha2, country.name), )

class SSLCertificationAuthority(models.Model):
    common_name = models.CharField(
        max_length=255,
        help_text="Common Name of the certification authority",
    )
    country_name = models.CharField(
        max_length=255,
        help_text="Country Name of the certification authority",
        choices=COUNTRIES,
        default="FR",
        blank=True,
    )
    locality_name = models.CharField(
        max_length=255,
        help_text="Locality of the certification authority",
        default="",
        blank=True,
    )
    state_name = models.CharField(
        max_length=255,
        help_text="State or province name of the certification authority",
        default="",
        blank=True,
    )
    organization_name = models.CharField(
        max_length=255,
        help_text="Organization name of the certification authority",
        default="",
        blank=True,
    )
    organization_unit_name = models.CharField(
        max_length=255,
        help_text="Organization unit name of the certification authority",
        default="",
        blank=True,
    )
    private_key = models.TextField(
        help_text="Private key of the CA",
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
    certificate = models.TextField(
        help_text="Certificate of the CA",
        default="",
        blank=True,
    )
    revocation_list = models.TextField(
        help_text="Revocation list of the certificate",
        default="",
        blank=True,
    )
    status = models.CharField(
        max_length=32,
        choices=(
            ('CREATED', 'Created'),
            ('GENERATING', 'Generating'),
            ('VALID', 'Valid'),
            ('INVALID', 'Invalid'),
        ),
        default="CREATED",
        blank=True,
    )

    expires_at = models.DateTimeField(help_text="Until when must the CA be valid. Format YYYY-MM-DD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.common_name

    class Meta:
        verbose_name = "SSL certification authority"
        verbose_name_plural = "SSL certification authorities"
