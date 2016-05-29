import re
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from account.forms import NoError
from account.views import is_moderator
from account.views import is_auth
from assessment.forms import QualityForm
from assessment.models import Quality, Assessment, QUALITY_CATEGORY
from account.models import Expert
from django.core.exceptions import ObjectDoesNotExist
from assessment.validator import validate_quality_id


@is_auth
def edit_assessments(request):
    user = Expert.objects.get(email=request.user.email)

    if request.method == "POST":
        for quality_id, point in request.POST.items():
            # TODO: Сделай валидаторы
            if re.match(r'\d+', str(quality_id)) and re.match(r'\d+', str(point)):
                Assessment.objects.update_or_create(expert=user,
                                                    quality=Quality.objects.get(id=quality_id),
                                                    defaults={"point": point})

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
    return render(request, 'assessment/assessments/assessments.html', {"assessments": Assessment.objects.all()})


def show_qualities(request):
    return render(request, 'assessment/qualities/qualities.html', {"qualities": Quality.objects.all()})


@is_moderator
def new_quality(request):
    q = Quality()
    q.save()
    return edit_quality(request, q.id)


@is_moderator
def edit_quality(request, id):
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

