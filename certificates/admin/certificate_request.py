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
from certificates.models import SSLCertificateRequest
from certificate import SSLCertificateAdmin

class SSLCertificateRequestAdmin(admin.ModelAdmin):
    list_display = (
        'common_name',
        'user',
        'country_name',
        'private_key_size',
        'status',
        'created_at',
        'updated_at',
        'signed_certificate'
    )
    date_hierarchy = 'created_at'
    ordering = (
        'common_name',
        'user',
        'country_name',
    )
    readonly_fields = ('private_key', 'request')
    search_fields = (
        'common_name',
        'user__username',
    )

admin.site.register(SSLCertificateRequest, SSLCertificateRequestAdmin)
