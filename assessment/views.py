from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from assessment.models import Quality, Assessment
from account.models import Expert
from django.core.exceptions import ObjectDoesNotExist


def show_qualities(request):
    if request.user.is_moderator:
        qualities = Quality.objects.all()
        return render(request, "assessment/qualities.html", {"qualities": qualities})
    else:
        return HttpResponse("вы не являетесь модератором")


def new_quality(request, quality_id=-1):
    if request.user.is_moderator:
        if request.method == "POST" and "quality" in request.POST:
            q = Quality.objects.get(id=quality_id)
            q.quality = request.POST["quality"]
            q.description = request.POST["description"]
            q.save()
            return HttpResponseRedirect("/qualities/")
        else:
            if quality_id == -1:
                q = Quality()
                q.save()
            else:
                q = Quality.objects.get(id=quality_id)
            return render(request, "assessment/quality.html", {"quality": q})
    else:
        return HttpResponse("вы не являетесь модератором")


def show_assessments(request):
    if request.user.is_expert:
        return render(request, 'assessment/assessments.html', {"qualities": Quality.objects.all()})
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

    return render(request, "assessment/assessment.html", {"quality": quality,
                                                          "point": point})

# Вытащил из account, хз зачем я их туда поместил
# def assessments(request):
#     if not request.user.is_authenticated():
#         return HttpResponseRedirect(reverse("account:login"))
#
#     if request.user.is_moderator:
#         return render(request, "account/assessments.html")
#
#     if request.user.is_expert:
#         return HttpResponseRedirect(reverse("account:cabinet"))
#
#     return HttpResponseRedirect("account:login")

# def qualities(request):
#     if not request.user.is_authenticated():
#         return HttpResponseRedirect(reverse("account:login"))
#
#     if request.user.is_moderator:
#         q = Quality.objects.all()
#         return render(request, "account/qualities.html", {"qualities": q})
#
#     if request.user.is_expert:
#         return HttpResponseRedirect(reverse("account:cabinet"))
#
#     return HttpResponseRedirect("account:login")
