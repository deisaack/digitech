from django.conf.urls import url

from . views import ProjectTemplateView, ProjectDetailView, ProjectListView

urlpatterns = [
    url(r'^project/$', ProjectTemplateView.as_view(), name='project'),
    url(r'^projects/all/$', ProjectListView.as_view(), name='all-project'),
    url(r'^(?P<pk>\d+)', ProjectDetailView.as_view(), name='project-detail'),
]
