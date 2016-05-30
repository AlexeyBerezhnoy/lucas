from django import forms
from django.core.exceptions import ValidationError
from assessment.models import QUALITY_CATEGORY, Quality
from assessment.validator import validate_quality_id, validate_point


class QualityForm(forms.Form):
    quality = forms.CharField(label="Название",
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.ChoiceField(label="Категория",
                                 choices=QUALITY_CATEGORY,
                                 widget=forms.Select(attrs={"class": "form-control"}))
    description = forms.CharField(label="Описание",
                                  widget=forms.Textarea(attrs={"class": "form-control"}))


class AssessmentForm(forms.Form):
    quality = forms.IntegerField()
    point = forms.IntegerField()

    def clean(self):
        validate_point(self.cleaned_data.get('point'))
        try:
            Quality.objects.get(id=self.cleaned_data.get('quality'))
        except Exception:
            raise ValidationError("Качество не найдено")
