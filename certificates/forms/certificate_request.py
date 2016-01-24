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

from django import forms
from certificates.models import SSLCertificateRequest, SSLCertificationAuthority

class SSLCertificateRequestForm(forms.ModelForm):
    private_key_password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="This password is used to encrypt the private key in the database. Choose a strong one!",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(SSLCertificateRequestForm, self ).__init__(*args, **kwargs)
        self.fields['certification_authority'].queryset = SSLCertificationAuthority.objects.filter(status="VALID")

    def configure(self, request):
        if  request.user.is_staff:
            self.fields['auto_sign'] = forms.BooleanField(
                help_text="If yes, this certificate will be automatically validated without any intervention from an admin.",
                required=False,
            )
            self.fields['server_certificate'] = forms.BooleanField(
                help_text="If checked, will generate a certificate for a server",
                required=False,
            )

    class Meta:
        model = SSLCertificateRequest
        fields = (
            'common_name',
            'certification_authority',
            'country_name',
            'locality_name',
            'state_name',
            'organization_name',
            'organization_unit_name',
            'private_key_size',
        )
