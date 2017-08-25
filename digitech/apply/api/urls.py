from django.conf.urls import include,url
from .views import ApplicationCreateApiView, ApplicationDetailApiView,\
    ApplicationDeleteApiView, ApplicationUpdateApiView, ApplicationListApiView

from django.contrib import admin


urlpatterns = [
    url(r'^$', ApplicationListApiView.as_view(), name='list'),
    ]
























urlpatterns +=[
    # url(r'^$', apply_power, name='apply'),
    # url(r'^new/$', ApplicationForm.as_view(), name='appli'),
    url(r'^create/$', ApplicationCreateApiView.as_view(), name='create'),
    # url(r'^u/$', ApplicationUpdateView.as_view(), name='update'),
    # url(r'^my-application/$', ApplicationListView.as_view(), name='all-project'),
    url(r'^(?P<pk>\d+)/$', ApplicationDetailApiView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/u/$', ApplicationUpdateApiView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/d/$', ApplicationDeleteApiView.as_view(), name='delete'),
    # url(r'^(?P<pk>\d+)/u/$', application_update, name='application-update'),
    # url(r'^pdf/$', GeneratePdf.as_view()),
    # url(r'^summary/$', views.Summary.as_view(), name='summary'),
    # url(r'^m/$', views.MyApplicationPdf.as_view(), name='pdf'),
]
