from django.conf.urls import url

from . views import ApplicationCreateView, ApplicationDetailView, photo_list, \
    ApplicationListView,  ApplicationForm, apply_power, ApplicationUpdateView, application_update, GeneratePdf
from . import views
urlpatterns = [
    url(r'^album$', photo_list, name='album'),
    url(r'^$', apply_power, name='apply'),
    url(r'^new/$', ApplicationForm.as_view(), name='appli'),
    url(r'^nw/$', ApplicationCreateView.as_view(), name='aply'),
    url(r'^u/$', ApplicationUpdateView.as_view(), name='update'),
    url(r'^my-application/$', ApplicationListView.as_view(), name='all-project'),
    url(r'^(?P<pk>\d+)/$', ApplicationDetailView.as_view(), name='application-detail'),
    url(r'^(?P<pk>\d+)/u/$', ApplicationUpdateView.as_view(), name='application-update'),
    # url(r'^(?P<pk>\d+)/u/$', application_update, name='application-update'),
    url(r'^pdf/$', GeneratePdf.as_view()),
    url(r'^summary/$', views.Summary.as_view(), name='summary'),
    url(r'^m/$', views.MyApplicationPdf.as_view(), name='pdf'),
]
