from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from assessment.models import Expert
from account.forms import NoError, LoginForm, InviteForm, ModeratorForm


# def add_menu_items(func):
#     def view(request, *args):
#         if request.user.is_moderator:
#             request.menu_items = [[["Профиль", "account:cabinet"]],
#                                   [["Експерты", "account:experts"],
#                                    ["Качества", "account:cabinet"],
#                                    ["Оценки", "account:cabinet"]]]
#         if request.user.is_expert:
#             request.menu_items = [[["Профиль", "account:cabinet"]],
#                                   [["Оценки", "account:cabinet"]]]
#         return func(request, *args)
#
#     return view


def is_auth(func):
    def view(request):
        if request.user.is_authenticated():
            return func(request)
        return HttpResponseRedirect(reverse("account:login"))
    return view


def is_moderator(func):
    @is_auth
    def view(request, *args):
        # Todo: убери is_admin
        if request.user.is_moderator or request.user.is_admin:
            return func(request, *args)

        if request.user.is_expert:
            return HttpResponseRedirect(reverse("account:cabinet"))
    return view


def is_expert(func):
    @is_auth
    def view(request, *args):
        if request.user.is_expert:
            return func(request, *args)

        if request.user.is_moderator:
            return HttpResponseRedirect(reverse("account:cabinet"))

    return view


# TODO: дай вьювам нормальные имена

@is_moderator
def invite_expert(request):
    if request.method == "POST":
        form = InviteForm(request.POST, error_class=NoError)
        if form.is_valid():
            try:
                # TODO с этим нужно что-то сделать, возможно переопределить конструктор класса Expert
                Expert.objects.create_expert(email=request.POST["email"],
                                             last_name=request.POST["last_name"],
                                             first_name=request.POST["first_name"],
                                             middle_name=request.POST["middle_name"],
                                             profession=request.POST["profession"],
                                             professional_experience=request.POST["professional_experience"],
                                             position=request.POST["position"],
                                             driver_license="A",
                                             driving_experience=2)
                return HttpResponseRedirect(reverse("account:cabinet"))
            except IntegrityError:
                form = InviteForm()

    else:
        form = InviteForm
    return render(request, "account/experts/new_expert.html", {"form": form})


@is_moderator
def show_expert(request, *args):
    expert = Expert.objects.get(id=args[0])
    return render(request, "account/experts/show_expert.html", {"expert": expert})


@is_moderator
def show_experts(request):
    experts = Expert.objects.filter(is_expert=True)
    return render(request, "account/experts/experts.html", {"experts": experts})


@is_auth
def cabinet(request):
    user = request.user
    # if user.is_moderator:
    form = ModeratorForm()
    return render(request, "account/profile/show_profile.html", {"user": user,
                                                    "form": form})


def my_login(request):
    if request.user.is_authenticated():
        logout(request)
    if request.method == "POST":
        form = LoginForm(request.POST, error_class=NoError, auto_id=False)
        if form.is_valid():
            user = authenticate(email=request.POST["email"],
                                password=request.POST["password"])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("account:cabinet"))

        error_message = "Пожалуйста введите правильные адрес электронной почты и пароль"
        return render(request, "account/login.html", {"error_message": error_message,
                                                      "form": form})
    else:
        form = LoginForm(auto_id=False)
    return render(request, "account/login.html", {"form": form})


# TODO: перенаправь ссылку
def confirm(request, email, password):
    user = authenticate(email=email, password=password)
    if user.is_active:
        return HttpResponseRedirect(reverse("account:cabinet"))
    else:
        user.is_active = True
        user.save()
        return HttpResponse("passive")
