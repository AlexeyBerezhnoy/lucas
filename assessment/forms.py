from django import forms
from assessment.models import QUALITY_CATEGORY


class QualityForm(forms.Form):
    quality = forms.CharField(label="Название",
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.ChoiceField(label="Категория",
                                 choices=QUALITY_CATEGORY,
                                 widget=forms.Select(attrs={"class": "form-control"}))
    description = forms.CharField(label="Описание",
                                  widget=forms.Textarea(attrs={"class": "form-control"}))
