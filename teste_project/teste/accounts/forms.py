from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django import forms

from home.forms import PrimatoModelForm, exclude_softdelete_fields
from accounts.models import Account


class CustomUserForm(UserCreationForm):

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()  # settings.AUTH_USER_MODEL
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class CustomUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)


class CustomUserReadonlyForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()  # settings.AUTH_USER_MODEL
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'last_login', ]


class CustomUserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()  # settings.AUTH_USER_MODEL
        fields = ['is_active', 'groups']


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()  # settings.AUTH_USER_MODEL
        fields = ['new_password1', 'new_password2']


class GroupForm(PrimatoModelForm):
    class Meta:
        model = Group
        fields = '__all__'
