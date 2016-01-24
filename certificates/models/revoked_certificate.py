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
import django.utils.timezone
from certification_authority import SSLCertificationAuthority

class SSLRevokedCertificate(models.Model):
    certification_authority = models.ForeignKey(
        SSLCertificationAuthority,
        on_delete=models.CASCADE,
        help_text="The certification authority that signed the certificate",
    )
    serial_number = models.IntegerField(
        help_text="Serial number of the certificate"
    )
    reason = models.CharField(
        max_length=32,
        choices=(
            ('UNSPECIFIED', 'Unspecified reason'),
            ('KEY_COMPROMISE', 'Key compromised'),
            ('CA_COMPROMISE', 'CA compromised'),
            ('AFFILIATION_CHANGED', 'Affiliation changed, CN changed'),
            ('SUPERSEDED', 'Certificate has been superseded'),
            ('CESSATION_OF_OPERATION', 'Cessation of operation'),
            ('PRIVILEGE_WITHDRAWN', 'Privileges withdrawn'),
            ('AA_COMPRIMISE', 'Attribute authority compromised'),
        ),
        default="UNSPECIFIED",
    )

    revocation_date = models.DateTimeField(
        default=django.utils.timezone.now,
        help_text="When is the certificate revoked ?"
    )

    def __unicode__(self):
        return u"%s 0x%X" % (self.certification_authority.common_name, self.serial_number)

    class Meta:
        verbose_name = "SSL revoked certificate"
        verbose_name_plural = "SSL revoked certificate"
        unique_together = (("certification_authority", "serial_number"),)
