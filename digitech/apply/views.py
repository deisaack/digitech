from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from . models import Application
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from digitech.operation.mixins import UserAuthorMixin
from . forms import PowerApplicationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from .forms import PowerApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from digitech.utils import render_to_pdf
from django.template.loader import get_template
from datetime import datetime
from digitech.operation import models
from django_countries import countries

User = get_user_model()


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    # template_name = 'operation/project_detail.html'
    model = Application

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['application_list'] = self.get_queryset()
        return context


class ApplicationListView(SuperuserRequiredMixin, ListView):
    model = Application


class ApplicationCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'apply/apply.html'
    form_class = PowerApplicationForm

    def form_valid(self, form):
        form.instance.author = self.request.user()
        return super(ApplicationCreateView, self).form_invalid(form)


class ApplicationDeleteView(UserAuthorMixin, generic.DeleteView):
    model = Application
    success_url = reverse_lazy('home')


class ApplicationUpdateView(generic.UpdateView):
    template_name = 'apply/update.html'
    model = Application
    form_class = PowerApplicationForm


class ApplicationForm(generic.FormView):
    form_class = PowerApplicationForm
    template_name = 'apply/apply.html'
    success_url = reverse_lazy('home')


@login_required
def apply_power(request):
    form = PowerApplicationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Your application was successfully submited, we will get in touch shortly")
        return redirect(reverse('apply:apply'))
    context = {
        "form": form,
        'title': 'Register a publisher'
    }
    return render(request, "apply/apply.html", context)


def application_update(request, pk=None):
    from django_countries import countries
    countries = list(countries)[:10]
    instance = get_object_or_404(Application, pk=pk)
    form = PowerApplicationForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Your application details were successfully updated", extra_tags='html_safe')
        return redirect(reverse('apply:apply'))

    context = {
        "instance": instance,
        "form": form,
        'countries': countries,
    }
    return render(request, "apply/update.html", context)


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('apply/pdf/invoice.html')
        context = {
            'today': datetime.now(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'invoice_id': 1233434,
        }
        pdf = render_to_pdf('apply/pdf/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("123")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class MyApplicationPdf(View):
    def get(self, request, *args, **kwargs):
        template = get_template('apply/pdf/application.html')
        user = request.user
        context = {
            'today': datetime.now(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'invoice_id': 1233434,
            'user': user
        }
        pdf = render_to_pdf('apply/pdf/application.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % user
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class Summary(View):
    def get(self, request, *args, **kwargs):
        application_list = Application.objects.all()
        user_list = User.objects.all()
        transformer_list = models.Transformer.objects.all()
        machinery_list = models.Machinery.objects.all()
        employee_list = models.Employee.objects.all()
        project_list = models.Project.objects.all()
        template = get_template('apply/pdf/summary.html')
        user = request.user
        context = {
            'today': datetime.now(),
            'application_list': application_list,
            'user_list': user_list,
            'transformer_list': transformer_list,
            'machinery_list': machinery_list,
            'employee_list': employee_list,
            'project_list': project_list,
            'user': user,
        }
        pdf = render_to_pdf('apply/pdf/summary.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            from django.utils import timezone
            now = datetime.now()
            filename = "summary-%s.pdf" % now
            content = "inline; filename='%s'" % filename
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse(""
                            "Not found")


from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm


def photo_list(request):
    photos = Photo.objects.all()
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()
    return render(request, 'album/photo_list.html', {'form': form, 'photos': photos})

