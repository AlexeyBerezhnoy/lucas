from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django import forms

from account.models import CATEGORIES


# Todo: это ужасный костыль, убери его
class NoError(ErrorList):
    def __str__(self):
        return ""


class LoginForm(forms.Form):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={"class": "form-control field-signin",
                                                           "placeholder": "email"}))
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={"class": "form-control field-signin",
                                                                 "placeholder": "пароль"}))


class ExpertForm(forms.Form):
    email = forms.EmailField(label="Email",
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Фамилия",
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="Имя",
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(label="Отчество",
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    profession = forms.CharField(label="Профессия",
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    professional_experience = forms.CharField(label="Стаж работы",
                                              widget=forms.TextInput(attrs={"class": "form-control"}))
    position = forms.CharField(label="Должность",
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    driver_license = forms.ChoiceField(label="Водительское удостоверние",
                                       choices=((cat, cat) for cat in CATEGORIES),
                                       widget=forms.Select(attrs={"class": "form-control"}))
    driving_experience = forms.CharField(label="Водительский стаж",
                                         widget=forms.TextInput(attrs={"class": "form-control"}))


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
