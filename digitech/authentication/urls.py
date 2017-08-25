from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^password-reset/$', views.PasswordResetView.as_view(),
        name='password-reset'),
    url(r'^password-reset-done/$', views.PasswordResetDoneView.as_view(),
        name='password-reset-done'),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$$', views.PasswordResetConfirmView.as_view(),  # NOQA
        name='password-reset-confirm'),
    url(r'^me/$', views.ShowProfile.as_view(), name='show_self'),
    url(r'^me/edit/$', views.EditProfile.as_view(), name='edit_self'),
    url(r'^(?P<slug>[\w\-]+)/$', views.ShowProfile.as_view(),
        name='show'),
]
