from django.forms import ModelForm
from django.forms.utils import ErrorList
from django import forms

from account.models import CATEGORIES, Moderator


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


class InviteForm(forms.Form):
    email = forms.EmailField()
    last_name = forms.CharField()
    first_name = forms.CharField()
    middle_name = forms.CharField()
    profession = forms.CharField()
    professional_experience = forms.CharField()
    position = forms.CharField()
    driver_license = forms.ChoiceField(choices=((cat, cat) for cat in CATEGORIES))
    driving_experience = forms.CharField()


class ModeratorForm(ModelForm):
    class Meta:
        model = Moderator
        fields = ['email', 'last_name', 'first_name', 'middle_name']
