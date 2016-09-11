from django import forms
from django.core.exceptions import ValidationError
from assessment.models import Quality
from assessment.validator import validate_point


class QualityForm(forms.ModelForm):
    class Meta:
        model = Quality
        fields = ['quality', 'category', 'description']

    def __init__(self, *args, **kwargs):
        super(QualityForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AssessmentForm(forms.Form):
    quality = forms.IntegerField()
    point = forms.IntegerField()

    def clean(self):
        validate_point(self.cleaned_data.get('point'))
        try:
            Quality.objects.get(id=self.cleaned_data.get('quality'))
        except Exception:
            raise ValidationError("Качество не найдено")
