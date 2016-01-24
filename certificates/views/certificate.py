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
from certificates.models import SSLCertificate, SSLRevokedCertificate
from certificates.tasks import regenerate_certificate_revocation_list

class ShowSSLCertificate(DetailView):
    model = SSLCertificate
    template_name = "certificate/certificate.html"
    context_object_name = "cert"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ShowSSLCertificate, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return SSLCertificate.objects.filter(pk=self.kwargs['pk'])
        else:
            return SSLCertificate.objects.filter(certificate_request__user=self.request.user, pk=self.kwargs['pk'])

    def get_object(self):
        return super(ShowSSLCertificate, self).get_object()

    def get_context_data(self, **kwargs):
        context = super(ShowSSLCertificate, self).get_context_data(**kwargs)
        return context

class ListSSLCertificate(ListView):
    model = SSLCertificate
    template_name = "certificate/certificate_list.html"
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListSSLCertificate, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return SSLCertificate.objects.all()
        else:
            return SSLCertificate.objects.filter(certificate_request__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ListSSLCertificate, self).get_context_data(**kwargs)
        return context

@staff_member_required
def revoke_certificate_view(request, pk):
    cert = get_object_or_404(SSLCertificate, pk=pk)
    if cert.status == 'VALID':
        cert.status='REVOKED'
        cert.save()
        revoked = SSLRevokedCertificate(
            certification_authority=cert.certification_authority,
            serial_number=cert.serial_number,
            reason="UNSPECIFIED",
        )
        revoked.save()
        regenerate_certificate_revocation_list.delay(cert.certification_authority)
    return redirect(reverse_lazy('show_certificate', kwargs={"pk":pk}))
