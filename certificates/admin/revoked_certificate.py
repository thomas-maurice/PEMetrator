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

from django.contrib import admin
from certificates.models import SSLRevokedCertificate

class SSLRevokedCertificateAdmin(admin.ModelAdmin):
    list_display = (
        'get_ca_common_name',
        'serial_number',
        'reason',
        'revocation_date',
    )
    date_hierarchy = 'revocation_date'
    ordering = (
        'serial_number',
        'reason',
        'certification_authority__common_name',
    )
    search_fields = (
        'reason',
        'serial_number',
    )

    def get_ca_common_name(self, cert):
        return cert.certification_authority.common_name
    get_ca_common_name.short_description = "CA Common name"

admin.site.register(SSLRevokedCertificate, SSLRevokedCertificateAdmin)
