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
from certificates.models import SSLCertificate

class SSLCertificateAdmin(admin.ModelAdmin):
    list_display = (
        'get_common_name',
        'get_user',
        'status',
        'created_at',
        'updated_at',
    )
    date_hierarchy = 'created_at'
    ordering = (
        'certificate_request__common_name',
        'certificate_request__user',
    )
    readonly_fields = ('certificate',)
    search_fields = (
        'get_common_name',
        'get_user',
    )

    def get_common_name(self, cert):
        return cert.certificate_request.common_name
    get_common_name.short_description = "Common name"

    def get_user(self, cert):
        return cert.certificate_request.user
    get_user.short_description = "User"

admin.site.register(SSLCertificate, SSLCertificateAdmin)
