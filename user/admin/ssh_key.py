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
from user.models import SSHPubKey

class SSHPubKeyAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'key_name',
        'key_fingerprint',
        'key_size',
        'key_type',
        'created_at',
        'updated_at',
    )
    fieldsets = (
        ('Key infos', {
            'classes': ['wide', 'extrapretty', ],
            'fields': (
                'user',
                'key_name',
            ),
        }),
        ('Key data', {
            'classes': ['wide', ],
            'fields': (
                'key_raw',
            )
        }),
    )
    date_hierarchy = 'created_at'
    ordering = (
        'user',
        'key_name',
        'created_at',
    )
    search_fields = (
        'user__username',
        'key_name',
        'key_fingerprint',
    )

admin.site.register(SSHPubKey, SSHPubKeyAdmin)
