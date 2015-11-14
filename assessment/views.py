from django.shortcuts import render
from .models import Expert, Quality, Assessment


def get_experts(request):
    experts = Expert.objects.all()
    return render(request, "assessment/expert.html", {'experts': experts})


def get_quality(request):
    quality = Quality.objects.all()
    return render(request, "assessment/quality.html", {'quality': quality})


def get_assessments(request):
    assessments = Assessment.objects.all()
    return render(request, "assessment/assessment.html", {'assessments': assessments})
