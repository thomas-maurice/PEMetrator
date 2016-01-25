# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-24 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sslcertificate',
            name='certificate_request',
            field=models.OneToOneField(help_text=b'The corresponding request', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='signed_certificate', to='certificates.SSLCertificateRequest'),
        ),
    ]