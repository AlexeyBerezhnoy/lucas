from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from account.forms import NoError
from account.views import is_moderator
from assessment.forms import QualityForm
from assessment.models import Quality, Assessment
from account.models import Expert
from django.core.exceptions import ObjectDoesNotExist


def show_qualities(request):
    qualities = Quality.objects.all()
    return render(request, "assessment/qualities/qualities.html", {"qualities": qualities})


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



def show_assessments(request):
    if request.user.is_moderator or request.user.is_admin:
        return render(request, 'assessment/assessments/assessments.html', {"assessments": Assessment.objects.all()})
    if request.user.is_expert:
        return render(request, 'assessment/assessments/assessments.html', {"qualities": Quality.objects.all()})
    else:
        return HttpResponse("вы не являетесь экспертом")


def new_assessment(request, quality_id):
    expert = Expert.objects.get(email=request.user.email)
    # Получить оценку текущего качество текущем экспертом
    try:
        Quality.objects.get(id=quality_id).assessment_set.get(expert=expert)
    # Оценки не сучествует
    except ObjectDoesNotExist:
        a = Assessment(quality=Quality.objects.get(id=quality_id),
                       expert=expert,
                       point=0)
        a.save()

    quality = Quality.objects.get(id=quality_id)
    point = quality.assessment_set.get(expert=expert).point

    if request.method == "POST" and "point" in request.POST:
        a = quality.assessment_set.get(expert=expert)
        a.point = int(request.POST["point"])
        a.save()
        return HttpResponseRedirect("/assessments/")

    return render(request, "assessment/assessments/assessment.html", {"quality": quality,
                                                                      "point": point})
