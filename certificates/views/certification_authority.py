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
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from certificates.forms import SSLCertificationAuthorityForm
from certificates.models import SSLCertificationAuthority
from certificates.tasks import initialize_certification_authority
class ListSSLCertificationAuthorities(ListView):
    model = SSLCertificationAuthority
    template_name = "certification_authority/certification_authority_list.html"
    paginate_by = 10
    queryset = SSLCertificationAuthority.objects.filter()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListSSLCertificationAuthorities, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListSSLCertificationAuthorities, self).get_context_data(**kwargs)
        return context

class ShowSSLCertificationAuthority(DetailView):
    model = SSLCertificationAuthority
    template_name = "certification_authority/certification_authority.html"
    context_object_name = "ca"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ShowSSLCertificationAuthority, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return SSLCertificationAuthority.objects.filter(pk=self.kwargs['pk'])

    def get_object(self):
        return super(ShowSSLCertificationAuthority, self).get_object()

    def get_context_data(self, **kwargs):
        context = super(ShowSSLCertificationAuthority, self).get_context_data(**kwargs)
        return context

class DeleteSSLCertificationAuthority(DeleteView):
    model = SSLCertificationAuthority
    template_name = "certification_authority/certification_authority_delete_form.html"
    success_url = reverse_lazy('list_certification_authorities')
    context_object_name = "ca"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(DeleteSSLCertificationAuthority, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(SSLCertificationAuthority, id=self.kwargs['pk'])

class CreateSSLCertificationAuthority(CreateView):
    model = SSLCertificationAuthority
    template_name = "certification_authority/certification_authority_create_form.html"
    form_class = SSLCertificationAuthorityForm
    success_url = reverse_lazy("list_certification_authorities")
    context_object_name = "ca"

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateSSLCertificationAuthority, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('show_certification_authority', kwargs={"pk":self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        initialize_certification_authority.apply(args=[self.object])
        return super(CreateSSLCertificationAuthority, self).form_valid(form)
