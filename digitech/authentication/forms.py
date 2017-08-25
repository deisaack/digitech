from __future__ import unicode_literals
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from . import models
from django import forms
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model

from digitech.settings import ALLOWED_SIGNUP_DOMAINS
from authtools import forms as authtoolsforms
from django.contrib.auth import forms as authforms


User = get_user_model()


def SignupDomainValidator(value):
    if '*' not in ALLOWED_SIGNUP_DOMAINS:
        try:
            domain = value[value.index("@"):]
            if domain not in ALLOWED_SIGNUP_DOMAINS:
                raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501

        except Exception:
            raise ValidationError('Invalid domain. Allowed domains on this network: {0}'.format(','.join(ALLOWED_SIGNUP_DOMAINS)))  # noqa: E501


def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]

    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a reserved word.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')


def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')


def UniqueUsernameIgnoreCaseValidator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this Username already exists.')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        help_text='Usernames may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters')  # noqa: E261
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm your password",
        required=True)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=75)

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password', ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsernamesValidator)
        self.fields['username'].validators.append(InvalidUsernameValidator)
        self.fields['username'].validators.append(
            UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['email'].validators.append(SignupDomainValidator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
        return self.cleaned_data



class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

from django_countries.widgets import CountrySelectWidget


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # Field('dob'),
            Field('phone'),
            # Field('address'),
            Field('bio'),
            Field('residence'),
            Field('country'),
            Field('id_no'),
            Field('phone_number'),
            Submit('update', 'Update', css_class="btn-success"),
            )

    class Meta:
        widgets = {'country': CountrySelectWidget()}
        model = models.Profile
        fields = ['phone', 'bio', 'country', 'residence', 'id_no', 'residence']


class PasswordResetForm(authtoolsforms.FriendlyPasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('email', placeholder="Enter email",
                  autofocus=""),
            Submit('pass_reset', 'Reset Password', css_class="btn-warning"),
            )


class SetPasswordForm(authforms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('new_password1', placeholder="Enter new password",
                  autofocus=""),
            Field('new_password2', placeholder="Enter new password (again)"),
            Submit('pass_change', 'Change Password', css_class="btn-warning"),
            )
