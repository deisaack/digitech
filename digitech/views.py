from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from user_sessions.models import Session


class HomePage(generic.TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['online'] = Session.objects.filter(user__isnull=False)
        return context


class AboutPage(generic.TemplateView):
    template_name = "about.html"


class GalleryPage(generic.TemplateView):
    template_name = "gallery/gallery.html"


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    template_name = 'core/cover.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)
