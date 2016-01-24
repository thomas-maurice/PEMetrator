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

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from user.models import SSHPubKey
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from user.forms import SSHPubKeyForm

class ListSSHPubKeys(ListView):
    model = SSHPubKey
    template_name = "ssh_key/ssh_key_list.html"
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListSSHPubKeys, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListSSHPubKeys, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return SSHPubKey.objects.filter(user=self.request.user)

class ShowSSHPubKey(DetailView):
    model = SSHPubKey
    template_name = "ssh_key/ssh_key.html"
    context_object_name = "k"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ShowSSHPubKey, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return SSHPubKey.objects.filter(pk=self.kwargs['pk'], user=self.request.user)

    def get_object(self):
        return super(ShowSSHPubKey, self).get_object()

    def get_context_data(self, **kwargs):
        context = super(ShowSSHPubKey, self).get_context_data(**kwargs)
        return context

class UpdateSSHPubKey(UpdateView):
    model = SSHPubKey
    template_name = "ssh_key/ssh_key_update_form.html"
    form_class = SSHPubKeyForm
    context_object_name = "k"

    def get_success_url(self):
        return reverse_lazy('show_ssh_key', kwargs={"pk":self.kwargs['pk']})

    def get_object(self, queryset=None):
        return get_object_or_404(SSHPubKey, id=self.kwargs['pk'])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateSSHPubKey, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        return super(UpdateSSHPubKey, self).form_valid(form)

class DeleteSSHPubKey(DeleteView):
    model = SSHPubKey
    template_name = "ssh_key/ssh_key_delete_form.html"
    success_url = reverse_lazy('list_ssh_key')
    context_object_name = "k"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteSSHPubKey, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(SSHPubKey, id=self.kwargs['pk'], user=self.request.user)

class CreateSSHPubKey(CreateView):
    model = SSHPubKey
    template_name = "ssh_key/ssh_key_create_form.html"
    form_class = SSHPubKeyForm
    success_url = reverse_lazy("list_ssh_key")
    context_object_name = "k"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateSSHPubKey, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('show_ssh_key', kwargs={"pk":self.object.id})

    def form_valid(self, form):
        #o = super(CreateSSHPubKey, self).form_valid(form)
        #self.object.user = self.request.user
        #print "obj:", o
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateSSHPubKey, self).form_valid(form)
