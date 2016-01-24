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
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from user.forms import UserFormUpdateAdmin, UserFormCreateAdmin

class ListUsers(ListView):
    model = User
    template_name = "user/user_list.html"
    paginate_by = 10
    queryset = User.objects.filter()

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ListUsers, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListUsers, self).get_context_data(**kwargs)
        return context

class ShowUser(DetailView):
    model = User
    template_name = "user/user.html"
    context_object_name = "u"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(ShowUser, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

    def get_object(self):
        return super(ShowUser, self).get_object()

    def get_context_data(self, **kwargs):
        context = super(ShowUser, self).get_context_data(**kwargs)
        return context

class UpdateUser(UpdateView):
    model = User
    template_name = "user/user_update_admin_form.html"
    form_class = UserFormUpdateAdmin
    context_object_name = "u"

    def get_success_url(self):
        return reverse_lazy('show_user', kwargs={"pk":self.kwargs['pk']})

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['pk'])

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateUser, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #form.instance.author = self.request.user
        return super(UpdateUser, self).form_valid(form)

class DeleteUser(DeleteView):
    model = User
    template_name = "user/user_delete_form.html"
    success_url = reverse_lazy('list_user')
    context_object_name = "u"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteUser, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['pk'])

class CreateUser(CreateView):
    model = User
    template_name = "user/user_create_form.html"
    form_class = UserFormCreateAdmin
    success_url = reverse_lazy("list_user")
    context_object_name = "u"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateUser, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('show_user', kwargs={"pk":self.object.id})

    def form_valid(self, form):
        self.object = form.save()
        self.object.set_password(form.cleaned_data['password'])
        return super(CreateUser, self).form_valid(form)
