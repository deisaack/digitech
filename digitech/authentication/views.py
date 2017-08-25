from __future__ import unicode_literals
import json
import urllib

from django.shortcuts import render, redirect
from django.conf import settings
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from digitech.authentication.forms import SignUpForm
from digitech.feeds.models import Feed
from django_countries import countries


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form': form})

        else:
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                User.objects.create_user(username=username, password=password,
                                         email=email)
                user = authenticate(username=username, password=password)
                login(request, user)
                welcome_post = '{0} has joined the network.'.format(user.username,
                                                                    user.username)
                feed = Feed(user=user, post=welcome_post)
                feed.save()
                return redirect('/')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            return redirect('/')
        #
        # username = form.cleaned_data.get('username')
        # email = form.cleaned_data.get('email')
        # password = form.cleaned_data.get('password')
        # User.objects.create_user(username=username, password=password,
        #                          email=email)
        # user = authenticate(username=username, password=password)
        # login(request, user)
        # welcome_post = '{0} has joined the network.'.format(user.username,
        #                                                     user.username)
        # feed = Feed(user=user, post=welcome_post)
        # feed.save()
        # return redirect('/')


    else:
        return render(request, 'authentication/signup.html',
                      {'form': SignUpForm()})


class ShowProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/show_profile.html"
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        if slug:
            profile = get_object_or_404(models.Profile, slug=slug)
            user = profile.user
        else:
            user = self.request.user
        if user == self.request.user:
            kwargs["editable"] = True
        kwargs["show_user"] = user
        return super(ShowProfile, self).get(request, *args, **kwargs)


class EditProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/edit_profile.html"
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if "user_form" not in kwargs:
            kwargs["user_form"] = forms.UserForm(instance=user)
        if "profile_form" not in kwargs:
            kwargs["profile_form"] = forms.ProfileForm(instance=user.profile)
        return super(EditProfile, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = forms.UserForm(request.POST, instance=user)
        profile_form = forms.ProfileForm(request.POST,
                                         request.FILES,
                                         instance=user.profile)
        if not (user_form.is_valid() and profile_form.is_valid()):
            messages.error(request, "There was a problem with the form. "
                           "Please check the details.")
            user_form = forms.UserForm(instance=user)
            profile_form = forms.ProfileForm(instance=user.profile)
            return super(EditProfile, self).get(request,
                                                user_form=user_form,
                                                profile_form=profile_form)
        user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        messages.success(request, "Profile details saved!")
        return redirect("profiles:show_self")

from authtools import views as authviews
from django.core.urlresolvers import reverse_lazy


class PasswordResetView(authviews.PasswordResetView):
    form_class = forms.PasswordResetForm
    template_name = 'accounts/password-reset.html'
    success_url = reverse_lazy('profiles:password-reset-done')
    subject_template_name = 'accounts/emails/password-reset-subject.txt'
    email_template_name = 'accounts/emails/password-reset-email.html'


class PasswordResetDoneView(authviews.PasswordResetDoneView):
    template_name = 'accounts/password-reset-done.html'


class PasswordResetConfirmView(authviews.PasswordResetConfirmAndLoginView):
    template_name = 'accounts/password-reset-confirm.html'
    form_class = forms.SetPasswordForm

