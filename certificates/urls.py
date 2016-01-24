from django.conf.urls import patterns, url
import django.contrib.auth.views

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

from certificates.views  import ListSSLCertificationAuthorities, \
    CreateSSLCertificationAuthority, \
    ShowSSLCertificationAuthority, \
    DeleteSSLCertificationAuthority, \
    CreateSSLCertificateRequest, \
    ShowSSLCertificate, ListSSLCertificate, \
    sign_certificate_request_view, decline_certificate_request_view, \
    ShowSSLCertificateRequest, ListSSLCertificateRequest, \
    revoke_certificate_view
from django.conf.urls import include

urlpatterns = [
    url(r'certification_authority/(?P<pk>\d+)$', ShowSSLCertificationAuthority.as_view(), name="show_certification_authority"),
    url(r'certification_authority/delete/(?P<pk>\d+)$', DeleteSSLCertificationAuthority.as_view(), name="delete_certification_authority"),
    url(r'certification_authority/create$', CreateSSLCertificationAuthority.as_view(), name="create_certification_authority"),
    url(r'certification_authorities?$', ListSSLCertificationAuthorities.as_view(), name="list_certification_authorities"),

    url(r'certificate_request/create$', CreateSSLCertificateRequest.as_view(), name="create_certificate_request"),
    url(r'certificate_request/(?P<pk>\d+)$', ShowSSLCertificateRequest.as_view(), name="show_certificate_request"),
    url(r'certificate_requests/(?P<page>[0-9]+)/$', ListSSLCertificateRequest.as_view(), name="list_certificate_requests"),
    url(r'certificate_request/sign/(?P<pk>\d+)$', sign_certificate_request_view, name="sign_certificate_request"),
    url(r'certificate_request/decline/(?P<pk>\d+)$', decline_certificate_request_view, name="decline_certificate_request"),

    url(r'certificate/(?P<pk>\d+)$', ShowSSLCertificate.as_view(), name="show_certificate"),
    url(r'certificate/revoke/(?P<pk>\d+)$', revoke_certificate_view, name="revoke_certificate"),
    url(r'certificates/(?P<page>[0-9]+)/$', ListSSLCertificate.as_view(), name="list_certificates"),
]
