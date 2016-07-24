import re
from enum import Enum

from django.contrib import messages
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import scipy
from account.forms import NoError
from account.views import is_moderator, is_auth
from assessment.forms import QualityForm, AssessmentForm
from assessment.math import math_func
from assessment.models import Quality, Assessment, QUALITY_CATEGORY
from account.models import Expert
from django.core.exceptions import ObjectDoesNotExist


@is_auth
def edit_assessments(request):
    user = Expert.objects.get(email=request.user.email)

    if request.method == "POST":
        message = ""
        for quality_id, point in request.POST.items():
            form = AssessmentForm({"quality": quality_id,
                                   "point": point})
            if form.is_valid():
                Assessment.objects.update_or_create(expert=user,
                                                    quality=Quality.objects.get(id=quality_id),
                                                    defaults={"point": point})
            else:
                message = "форма не валидна"

        if message:
            messages.info(request, message)

    need_assessment = 0
    qualities = {}
    for category in QUALITY_CATEGORY:
        quality_set = Quality.objects.filter(category=category[0])
        quality_set.not_assessment = 0
        for quality in quality_set:
            try:
                quality.point = Assessment.objects.get(expert=user, quality=quality).point
            except ObjectDoesNotExist:
                quality_set.not_assessment += 1
                need_assessment += 1
        qualities[category[1]] = quality_set
    if need_assessment:
        messages.info(request, "Пожалуйста оцените ещё %d качеств" % need_assessment)
    return render(request, "assessment/assessments/show_assessments.html", {"qualities": qualities})


@is_moderator
def show_assessments(request):
    if request.method == "GET":
        return render(request, 'assessment/assessments/assessments.html', {"assessments": Assessment.objects.all()})
    if request.method == "JSON":
        categories = [quality.quality for quality in Quality.objects.all()]
        series = []

        qualities = Quality.objects.all()
        for quality in qualities:
            s = {'data': [[a.point, categories.index(quality.quality)] for a in quality.assessment_set.all()]}
            series.append(s)
        result = {
            "categories": categories,
            "series": series
        }
        return JsonResponse(result, safe=False)


def show_qualities(request):
    qualities = Quality.objects.all()

    # Найти согласованость
    table = []
    for e in Expert.objects.all():
        if e.is_expert and e.is_active:
            assessments = []
            mask = []
            for q in qualities:
                try:
                    assessments.append(Assessment.objects.get(expert=e, quality=q).point)
                    mask.append(0)
                except Exception:
                    assessments.append(0)
                    mask.append(1)
            masked_assessments = scipy.ma.array(assessments, mask=mask)
            table.append(masked_assessments)

    if table:
        coherence = math_func(table)
    else:
        coherence = False
    return render(request, 'assessment/qualities/qualities.html', {"qualities": qualities,
                                                                   "coherence": coherence})


@is_moderator
def new_quality(request):
    q = Quality()
    q.save()
    return edit_quality(request, q.id)


@is_moderator
def edit_quality(request, id):
    try:
        q = Quality.objects.get(id=id)
        if request.method == "POST":
            form = QualityForm(request.POST, error_class=NoError)
            if form.is_valid():
                q.quality = request.POST["quality"]
                q.category = request.POST["category"]
                q.description = request.POST["description"]
                q.save()
                return HttpResponseRedirect(reverse("assessment:qualities"))
            else:
                messages.error(request, "Форма не валидна")
                return render(request, "assessment/qualities/quality.html", {"quality": q,
                                                                             "form": form})
    except Exception:
        messages.error(request, "Качество не найден")

    form = QualityForm({"quality": q.quality,
                        "category": q.category,
                        "description": q.description},
                       error_class=NoError)

    return render(request, "assessment/qualities/quality.html", {"quality": q,
                                                                 "form": form})


@is_moderator
def del_quality(request, id):
    try:
        q = Quality.objects.get(id=id)
        q.delete()
        messages.success(request, "Качество удалено")
        # Todo: Отлови нормальное исключение
    except Exception:
        messages.error(request, "Качество не найден")
    return HttpResponseRedirect(reverse("assessment:qualities"))
