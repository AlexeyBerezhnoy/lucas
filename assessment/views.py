from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import DeletionMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.forms import formset_factory
from django.shortcuts import render
from assessment.forms import QualityForm, AssessmentForm
from assessment.models import Quality, Assessment, QUALITY_CATEGORY
from account.models import Expert


# TODO: это нужно пределать
class RateQualities(TemplateView):
    form = formset_factory(AssessmentForm)
    model = Assessment
    template_name = 'assessment/assessments/show_assessments.html'

    def get_context_data(self, **kwargs):
        ctx = super(RateQualities, self).get_context_data(**kwargs)
        qualities = {}
        for category in QUALITY_CATEGORY:
            quality_set = Quality.objects.filter(category=category[0])
            for quality in quality_set:
                try:
                    quality.point = Assessment.objects.get(expert=self.request.user, quality=quality).point
                except ObjectDoesNotExist:
                    pass
            qualities[category[1]] = quality_set
        ctx['qualities'] = qualities
        return ctx

    def post(self, request):
        for quality_id, point in request.POST.items():
            form = AssessmentForm({"quality": quality_id,
                                   "point": point})
            if form.is_valid():
                expert = Expert.objects.get(email=request.user.email)
                Assessment.objects.update_or_create(expert=expert,
                                                    quality=Quality.objects.get(id=quality_id),
                                                    defaults={"point": point})

        return render(request, "assessment/assessments/show_assessments.html", self.get_context_data())


class QualityList(ListView):
    model = Quality
    template_name = 'assessment/qualities/index.html'
    context_object_name = 'qualities'


class CreateQuality(CreateView):
    model = Quality
    form_class = QualityForm
    template_name = 'assessment/qualities/create.html'
    success_url = reverse_lazy('assessment:qualities')


class EditQuality(UpdateView):
    model = Quality
    form_class = QualityForm
    template_name = 'assessment/qualities/edit.html'
    success_url = reverse_lazy('assessment:qualities')


class DeleteQuality(DeletionMixin, BaseDetailView):
    model = Quality
    success_url = reverse_lazy('assessment:qualities')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
