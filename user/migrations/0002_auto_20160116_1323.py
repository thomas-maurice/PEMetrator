# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 13:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sshpubkey',
            name='key_fingerprint',
            field=models.CharField(editable=False, help_text=b'Fingerprint of the key', max_length=64),
        ),
        migrations.AlterField(
            model_name='sshpubkey',
            name='key_raw',
            field=models.TextField(help_text=b"Raw form of the public key. Of the form 'ssh-type key name'."),
        ),
        migrations.AlterField(
            model_name='sshpubkey',
            name='key_size',
            field=models.IntegerField(editable=False, help_text=b'Length in bits of the associated private key'),
        ),
        migrations.AlterField(
            model_name='sshpubkey',
            name='key_type',
            field=models.CharField(editable=False, help_text=b'Type of the SSH key', max_length=64),
        ),
        migrations.AlterField(
            model_name='sshpubkey',
            name='user',
            field=models.ForeignKey(help_text=b'Owner of the key', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='birth_date',
            field=models.DateField(help_text=b'Date of birth of the user', null=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user',
            field=models.OneToOneField(help_text=b'User owning this profile', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
