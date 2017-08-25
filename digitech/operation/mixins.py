from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from . models import Project


class PublicProjectMixin(object):
    query_set = Project.objects.all()


class AuthRequiredMixin(object):
    login_url = settings.LOGIN_URL
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path, self.login_url())
        return super(AuthRequiredMixin, self).dispatch(request, *args, **kwargs)


class UserAuthorMixin(AuthRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.id is not request.get_object():
            raise PermissionDenied
        return super(UserAuthorMixin, self).dispatch(request, *args, **kwargs)

# class UserAuthorMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.id is not request.get_object():
#             raise PermissionDenied
#         return super(UserAuthorMixin, self).dispatch(self, request, *args, **kwargs)



