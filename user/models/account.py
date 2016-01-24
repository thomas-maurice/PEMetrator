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

class UserAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, help_text="User owning this profile", on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, help_text="Date of birth of the user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def create_user_account(sender, instance, created, **kwargs):
    if created:
        UserAccount.objects.create(user=instance)

post_save.connect(create_user_account, sender=settings.AUTH_USER_MODEL)
