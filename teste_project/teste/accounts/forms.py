from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, HTML, LayoutObject, BaseInput, Fieldset, Row, \
    Column, ButtonHolder
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, UserChangeForm, \
    UsernameField
from django import forms
from django.forms import ModelForm


class CustomUserForm(UserCreationForm):

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()  # settings.AUTH_USER_MODEL
        fields = ['email', 'first_name', 'last_name',  'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.all().wrap(Div, css_class='col-6')

class CustomUserLoginForm(AuthenticationForm):
    username = UsernameField(required=False)  # Campo Email
    password = forms.CharField(label="Senha", strip=False, widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                AppendedText('username', '@fiocruz.br'),
                Field('password'),
                css_class='col-xl-6')
        )


class CustomUserReadonlyForm(ModelForm):
    first_name = forms.CharField(label='Nome', required=False)
    last_name = forms.CharField(label='Sobrenome', required=False)
    email = forms.CharField(label='Email', required=False)
    date_joined = forms.DateTimeField(label='Data de criação', required=False, )

    # last_login = forms.CharField(label='Último login', required=False)

    class Meta:
        model = get_user_model()  # settings.AUTH_USER_MODEL
        fields = ['first_name', 'last_name', 'email', 'date_joined', 'last_login']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        self.helper.all().wrap(Field, readonly='readonly', disabled='disabled')
        self.helper.all().wrap(Div, css_class='col-6')


class CustomUserUpdateForm(UserChangeForm):
    password = None
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                            widget=forms.CheckboxSelectMultiple(), label='Grupos')

    class Meta:
        model = get_user_model()  # settings.AUTH_USER_MODEL
        fields = ['is_active', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.all().wrap(Div, css_class='col-6')


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()  # settings.AUTH_USER_MODEL
        fields = ['new_password1', 'new_password2']


class GroupForm(forms.ModelForm):
    # sobrescrever a forma de exibição
    name = forms.CharField(label='Nome')
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),
                                                 widget=forms.CheckboxSelectMultiple(), label='Permissões')

    class Meta:
        model = Group
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_tag = False
    #     self.helper.form_class = 'row'
    #     self.helper.all().wrap(Div, css_class='col-6')
    #     self.helper.layout.append(
    #         Submit('salvar', 'Salvar', css_class="btn btn-primary btn btn-primary btn-lg btn-block"))
    #     self.helper.layout.append(HTML(
    #         '{% if form.initial.id and not is_view %}<input type="button" name="excluir" value="Excluir" class="btn btn btn-danger btn-lg btn-block" id="group_delete_button">{% endif %}'))
    #     self.helper.layout.append(self.helper.filter(Submit, HTML).wrap(Div, css_class='col-3'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            'name',
            'permissions',
        )
        self.helper.all().wrap(Div, css_class="col-6")
