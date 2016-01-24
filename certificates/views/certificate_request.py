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
from certificates.forms import SSLCertificateRequestForm
from certificates.models import SSLCertificateRequest
from certificates.tasks import create_certificate_request, sign_certificate_request

class ShowSSLCertificateRequest(DetailView):
    model = SSLCertificateRequest
    template_name = "certificate_request/certificate_request.html"
    context_object_name = "csr"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ShowSSLCertificateRequest, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return SSLCertificateRequest.objects.filter(pk=self.kwargs['pk'])
        else:
            return SSLCertificateRequest.objects.filter(user=self.request.user, pk=self.kwargs['pk'])

    def get_object(self):
        return super(ShowSSLCertificateRequest, self).get_object()

    def get_context_data(self, **kwargs):
        context = super(ShowSSLCertificateRequest, self).get_context_data(**kwargs)
        return context

class CreateSSLCertificateRequest(CreateView):
    model = SSLCertificateRequest
    template_name = "certificate_request/certificate_request_create_form.html"
    form_class = SSLCertificateRequestForm
    context_object_name = "csr"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateSSLCertificateRequest, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('show_certificate_request', kwargs={"pk":self.object.id})

    def get_form(self, form_class=SSLCertificateRequestForm):
        form = super(CreateSSLCertificateRequest, self).get_form(form_class)
        form.configure(self.request)
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        auto_sign=False
        if self.request.user.is_staff:
            if "auto_sign" in form.cleaned_data:
                auto_sign = form.cleaned_data['auto_sign']
            if "server_certificate"in form.cleaned_data:
                self.object.server_certificate = form.cleaned_data['server_certificate']
        self.object.save()
        create_certificate_request.delay(self.object, form.cleaned_data['private_key_password'], auto_sign)
        return super(CreateSSLCertificateRequest, self).form_valid(form)

class ListSSLCertificateRequest(ListView):
    model = SSLCertificateRequest
    template_name = "certificate_request/certificate_request_list.html"
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListSSLCertificateRequest, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return SSLCertificateRequest.objects.all()
        else:
            return SSLCertificateRequest.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ListSSLCertificateRequest, self).get_context_data(**kwargs)
        return context


@staff_member_required
def sign_certificate_request_view(request, pk):
    csr = get_object_or_404(SSLCertificateRequest, pk=pk)
    sign_certificate_request.delay(csr)
    return redirect(reverse_lazy('show_certificate_request', kwargs={"pk":pk}))

@staff_member_required
def decline_certificate_request_view(request, pk):
    csr = get_object_or_404(SSLCertificateRequest, pk=pk)
    if csr.status == 'VALIDATING':
        csr.status='DECLINED'
        csr.save()
    return redirect(reverse_lazy('show_certificate_request', kwargs={"pk":pk}))
