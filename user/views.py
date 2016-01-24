# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from user.forms import LoginForm
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
