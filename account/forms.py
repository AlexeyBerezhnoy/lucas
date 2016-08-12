from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms

from account.models import Expert, MyUser


class LoginForm(forms.Form):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={"class": "form-control field-signin",
                                                           "placeholder": "email"}))
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={"class": "form-control field-signin",
                                                                 "placeholder": "пароль"}))

    def get_user(self):
        return authenticate(**self.cleaned_data)

    def clean(self):
        user = self.get_user()
        if not user or user.is_anonymous():
            raise ValidationError('Заданный пользователь не существует')


class ExpertForm(forms.ModelForm):
    class Meta:
        model = Expert
        fields = ['email', 'last_name', 'first_name', 'middle_name',
                  'profession', 'professional_experience', 'position',
                  'driver_license', 'driving_experience']
        widgets = {
            'professional_experience': forms.TextInput(),
            'driving_experience': forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        super(ExpertForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ModeratorForm(forms.Form):
    email = forms.EmailField(label="Email",
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Фамилия",
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="Имя",
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(label="Отчество",
                                  widget=forms.TextInput(attrs={"class": "form-control"}))


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label="Старый пароль",
                                   widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password = forms.CharField(label="Новый пароль",
                                   widget=forms.PasswordInput(attrs={"class": "form-control"}))
    repeat_password = forms.CharField(label="Повторите новый пароль",
                                      widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean(self):
        if self.cleaned_data.get('new_password') != self.cleaned_data.get('repeat_password'):
            raise ValidationError("Введёные пароли не совпадают")


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Email",
                             widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean(self):
        if not MyUser.objects.filter(**self.cleaned_data):
            raise ValidationError('Заданный пользователь не найден')

    def get_user(self):
        return MyUser.objects.get(**self.cleaned_data)
