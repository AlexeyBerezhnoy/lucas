from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.shortcuts import render
from .models import MyUser


# def invite_moderator(request):
#     if request.method == "POST" and "email" in request.POST:
#         new_moderator = MyUser.objects.create_moderator(request.POST["email"],
#                                                         request.POST["last_name"],
#                                                         request.POST["first_name"],
#                                                         request.POST["middle_name"],)
#         new_moderator.save()
#         return HttpResponseRedirect("/account/invite_moderator")
#     return render(request, "account/invite_moderator.html")


#TODO: перенаправь ссылку
def confirm(request, email, password):
    user = authenticate(email=email, password=password)
    if user.is_active:
        return HttpResponse("active")
    else:
        user.is_active = True
        user.save()
        return HttpResponse("passive")
