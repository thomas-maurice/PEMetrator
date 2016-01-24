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

from user.views  import ListUsers, CreateUser, ShowUser, DeleteUser, UpdateUser
from user.views  import ListSSHPubKeys, CreateSSHPubKey, ShowSSHPubKey, DeleteSSHPubKey, UpdateSSHPubKey
from django.conf.urls import include

"""
    url(r'^login$', django.contrib.auth.views.login, {"template_name": "login/login.html"}, name="login"),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {"template_name": "login/login.html", 'next_page': 'login'},
        name="logout"),
    url(r'^password_change$',
        django.contrib.auth.views.password_change,
        {"template_name": "login/password_change_form.html", "post_change_redirect": "password_change_done"},
        name="pwchange"),
    url(r'^password_change_done$',
        django.contrib.auth.views.password_change_done,
        {"template_name": "login/password_change_done.html"},
        name="password_change_done"),
"""

urlpatterns = [
    url(r'^registration/', include('registration.backends.hmac.urls')),

    url(r'user/(?P<pk>\d+)$', ShowUser.as_view(), name="show_user"),
    url(r'user/update/(?P<pk>\d+)$', UpdateUser.as_view(), name="update_user"),
    url(r'user/delete/(?P<pk>\d+)$', DeleteUser.as_view(), name="delete_user"),
    url(r'user/create$', CreateUser.as_view(), name="create_user"),
    url(r'users?$', ListUsers.as_view(), name="list_user"),

    url(r'ssh_key/(?P<pk>\d+)$', ShowSSHPubKey.as_view(), name="show_ssh_key"),
    url(r'ssh_key/update/(?P<pk>\d+)$', UpdateSSHPubKey.as_view(), name="update_ssh_key"),
    url(r'ssh_key/delete/(?P<pk>\d+)$', DeleteSSHPubKey.as_view(), name="delete_ssh_key"),
    url(r'ssh_key/create$', CreateSSHPubKey.as_view(), name="create_ssh_key"),
    url(r'ssh_keys?$', ListSSHPubKeys.as_view(), name="list_ssh_key"),
]
