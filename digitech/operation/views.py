from django.views.generic import TemplateView, DetailView, ListView, RedirectView
from . models import Project
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from . mixins import UserAuthorMixin, AuthRequiredMixin
from user_sessions.models import Session

class ProjectTemplateView(TemplateView):
    template_name = 'operation/projects.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectTemplateView, self).get_context_data(**kwargs)
        context['title'] = "These are all Projects"
        context['name'] = "Feel ok Man"
        context['online'] = Session.objects.all()
        return context


class ProjectDetailView(DetailView):
    # template_name = 'operation/project_detail.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['project_list'] = self.get_queryset()
        return context


class ProjectListView(ListView):
    model = Project


class ProjectCreateView(AuthRequiredMixin, generic.CreateView):
    template_name = 'project/project_create.html'
    # form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user()
        return super(ProjectCreateView, self).form_invalid(form)


class ProjectDeleteView(UserAuthorMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy('home')


class ProjectUpdateView(UserAuthorMixin, generic.UpdateView):
    template_name = 'project/project_update.html'
    model = Project
    # form_class = ArticleForm
