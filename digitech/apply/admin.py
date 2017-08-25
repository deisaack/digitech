import django
from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User

    def get_user_model():
        return User

from user_sessions.templatetags.user_sessions import device, location

from .models import Application


class PaidApplications(admin.SimpleListFilter):
    title = _('Payment Status')
    parameter_name = 'paid'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Paid')),
            ('0', _('Not Paid'))
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(amount__gte=100).filter(installation=None)
        elif self.value() == '0':
            return queryset.filter(amount__lt=100).filter(installation=None)


class Instalation(admin.SimpleListFilter):
    title = _('Installation status')
    parameter_name = 'installation'

    def lookups(self, request, model_admin):
        return (
            ('instaled', _('installation')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'instaled':
            return queryset.filter(installation=None)


class SessionAdmin(admin.ModelAdmin):
    list_display = 'user','payment_method', 'amount', 'installation',
    search_fields = ()
    list_filter = PaidApplications, Instalation
    raw_id_fields = 'user',
    exclude = 'message',

    def __init__(self, *args, **kwargs):
        super(SessionAdmin, self).__init__(*args, **kwargs)
        if not self.search_fields and django.VERSION[:2] < (1, 7):
            self.search_fields = self.get_search_fields(None)

    def get_search_fields(self, request):
        User = get_user_model()
        return ('user', 'amount')


admin.site.register(Application, SessionAdmin)
