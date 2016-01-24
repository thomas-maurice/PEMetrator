# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
import sshpubkeys

class SSHPubKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Owner of the key")
    key_raw = models.TextField(help_text="Raw form of the public key. Of the form 'ssh-type key name'.")
    key_fingerprint = models.CharField(max_length=64, help_text="Fingerprint of the key", editable=False)
    key_size = models.IntegerField(help_text="Length in bits of the associated private key", editable=False)
    key_type = models.CharField(max_length=64, help_text="Type of the SSH key", editable=False)
    key_name = models.CharField(max_length=256, help_text="Explanatory name of the key")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "SSH public key"
        verbose_name_plural = "SSH public keys"

def update_ssh_key(sender, instance, **kwargs):
    key = sshpubkeys.SSHKey(instance.key_raw)
    instance.key_fingerprint = key.hash()
    instance.key_size = key.bits
    instance.key_type = key.key_type

pre_save.connect(update_ssh_key, sender=SSHPubKey)
