from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from account.models import MyUser
from assessment.models import Expert
from account.forms import NoError, LoginForm, ExpertForm, ModeratorForm, PasswordChangeForm
from django.contrib import messages


def is_auth(func):
    def view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse("account:login"))

    return view


def is_moderator(func):
    @is_auth
    def view(request, *args, **kwargs):
        if request.user.is_moderator:
            return func(request, *args, **kwargs)
        if request.user.is_expert:
            return HttpResponseRedirect(reverse("account:cabinet"))
        return HttpResponseRedirect(reverse("account:login"))

    return view


def is_expert(func):
    @is_auth
    def view(request, *args, **kwargs):
        if request.user.is_expert:
            return func(request, *args, **kwargs)
        if request.user.is_moderator:
            return HttpResponseRedirect(reverse("account:cabinet"))
        return HttpResponseRedirect(reverse("account:login"))

    return view


# TODO: дай вьювам нормальные имена


@is_auth
def show_profile(request):
    user = request.user
    profile = MyUser.objects.get(email=user.email)
    profile_form = "Отсутсвует информация"
    if user.is_moderator:
        profile_form = ModeratorForm({"email": profile.email,
                                      "last_name": profile.last_name,
                                      "first_name": profile.first_name,
                                      "middle_name": profile.middle_name},
                                     error_class=NoError)
    elif user.is_expert:
        profile_form = ExpertForm({"email": profile.email,
                                   "last_name": profile.last_name,
                                   "first_name": profile.first_name,
                                   "middle_name": profile.middle_name,
                                   "profession": profile.profession,
                                   "professional_experience": profile.professional_experience,
                                   "position": profile.position,
                                   "driver_license": profile.driver_license,
                                   "driving_experience": profile.driving_experience},
                                  error_class=NoError)
    password_change_form = PasswordChangeForm()
    return render(request, "account/profile/show_profile.html", {"profile": profile,
                                                                 "profile_form": profile_form,
                                                                 "password_change_form": password_change_form})


@is_auth
def edit_profile(request):
    user = request.user
    profile = MyUser.objects.get(email=user.email)
    if request.method == "POST":
        if user.is_moderator:
            form = ModeratorForm(request.POST)
            if form.is_valid():
                profile.email = request.POST["email"]
                profile.first_name = request.POST["first_name"]
                profile.last_name = request.POST["last_name"]
                profile.middle_name = request.POST["middle_name"]
                profile.save()
                messages.success(request, 'Информация не валидна.')
            else:
                messages.error(request, 'Форма не валидна')
        elif user.is_expert:
            form = ModeratorForm(request.POST)
            if form.is_valid():
                profile.email = request.POST["email"]
                profile.first_name = request.POST["first_name"]
                profile.last_name = request.POST["last_name"]
                profile.middle_name = request.POST["middle_name"]
                profile.save()
                messages.success(request, 'Информация не валидна.')
            else:
                messages.error(request, 'Форма не валидна')
    else:
        messages.error(request, 'Форма не заполнена')
    return HttpResponseRedirect(reverse("account:cabinet"))


@is_auth
def change_password(request):
    profile = MyUser.objects.get(email=request.user.email)
    email = request.user.email
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            if profile.check_password(request.POST["old_password"]):
                logout(request)
                profile.set_password(request.POST["new_password"])
                profile.save()
                user = authenticate(email=email,
                                    password=request.POST["new_password"])
                login(request, user)
                messages.success(request, 'Пароль успешно изменён')
            else:
                messages.error(request, 'Старый пароль введен неверно')
        else:
            messages.error(request, 'Некорректно заполненая форма')
    return HttpResponseRedirect(reverse("account:cabinet"))


@is_moderator
def new_expert(request):
    if request.method == "POST":
        form = ExpertForm(request.POST, error_class=NoError)
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
                password = get_new_password()
                e = Expert.objects.get(email=request.POST["email"])
                e.set_password(password)
                e.save()
                messages.success(request, "Пользователь добавлен")

                subject = "Пароль обновлён"
                ctx = {'request': request, 'user': e, 'password': password}
                message = render_to_string('account/email/invite_expert.html', ctx)
                send_message(e.email, subject, message)
                return HttpResponseRedirect(reverse("account:experts"))
            except IntegrityError:
                messages.error(request, "email занят")
    else:
        form = ExpertForm()
    return render(request, "account/experts/new_expert.html", {"form": form})


@is_moderator
def show_expert(request, id):
    try:
        expert = Expert.objects.get(id=id)
        form = ExpertForm({"email": expert.email,
                           "last_name": expert.last_name,
                           "first_name": expert.first_name,
                           "middle_name": expert.middle_name,
                           "profession": expert.profession,
                           "professional_experience": expert.professional_experience,
                           "position": expert.position,
                           "driver_license": expert.driver_license,
                           "driving_experience": expert.driving_experience})
    # Todo: Отлови нормальное исключение
    except Exception:
        messages.error(request, "Заданный пользователь не найден")
        return HttpResponseRedirect(reverse("account:experts"))
    return render(request, "account/experts/show_expert.html", {"expert": expert,
                                                                "form": form})


@is_moderator
def edit_expert(request, id):
    try:
        expert = Expert.objects.get(id=id)
        if request.method == "POST":
            form = ExpertForm(request.POST)
            if form.is_valid():
                expert.email = request.POST["email"]
                expert.first_name = request.POST["first_name"]
                expert.last_name = request.POST["last_name"]
                expert.middle_name = request.POST["middle_name"]
                expert.profession = request.POST["profession"]
                expert.professional_experience = request.POST["professional_experience"]
                expert.position = request.POST["position"]
                expert.driver_license = request.POST["driver_license"]
                expert.driving_experience = request.POST["driving_experience"]
                expert.save()
    except Exception:
        messages.error(request, "Заданный пользователь не найден")

    return HttpResponseRedirect(reverse("account:experts"))


@is_moderator
def del_expert(request, id):
    try:
        expert = Expert.objects.get(id=id)
        expert.delete()
        messages.success(request, "Пользователь удалён")
        # Todo: Отлови нормальное исключение
    except Exception:
        messages.error(request, "Заданный пользователь не найден")
    return HttpResponseRedirect(reverse("account:experts"))


@is_moderator
def toggle_activity(request, id):
    try:
        expert = Expert.objects.get(id=id)
        if expert.is_active:
            expert.is_active = False
            messages.success(request, "Пользователь заморожен")
        else:
            expert.is_active = True
            messages.success(request, "Пользователь разморожен")
        expert.save()
        # Todo: Отлови нормальное исключение
    except Exception:
        messages.error(request, "Заданный пользователь не найден")
    return HttpResponseRedirect(reverse("account:experts"))


@is_moderator
def show_experts(request):
    experts = Expert.objects.filter(is_expert=True)
    return render(request, "account/experts/experts.html", {"experts": experts})


def reset_password(request, email):
    request = generate_random_password(request, email)
    return HttpResponseRedirect(reverse("account:experts"))


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

        messages.error(request, 'Введите правильные логин и пароль.')
        return render(request, "account/login.html", {"form": form})
    else:
        form = LoginForm(auto_id=False)
    return render(request, "account/login.html", {"form": form})


def forgot_password(request):
    if request.user.is_authenticated():
        logout(request)
    if request.method == "POST":
        form = LoginForm(request.POST, error_class=NoError, auto_id=False)
        # TODO: добавь проверку
        if form:
            request = generate_random_password(request, request.POST["email"])
            return HttpResponseRedirect(reverse("account:login"))
    else:
        form = LoginForm(auto_id=False)
    return render(request, "account/forgot_password.html", {"form": form})


# TODO: перенаправь ссылку
def confirm(request, email, password):
    user = authenticate(email=email, password=password)
    if user.is_active:
        return HttpResponseRedirect(reverse("account:cabinet"))
    else:
        user.is_active = True
        user.save()
        return HttpResponse("passive")


# Todo: Использовать здесь request не лучшая идея
def generate_random_password(request, email):
    try:
        user = MyUser.objects.get(email=email)
        password = get_new_password()
        user.set_password(password)
        user.save()
        messages.success(request, "Пароль обновлён")

        subject = "Пароль обновлён"
        ctx = {'request': request, 'user': user, 'password': password}
        message = render_to_string('account/email/new_password.html', ctx)
        send_message(email, subject, message)
    except Exception:
        messages.error(request, "Заданный пользователь не найден")
    return request


def get_new_password(length=4):
    return MyUser.objects.make_random_password(length=length, allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZ')


def send_message(email, subject, message):
    send_mail(subject, message, 'admin@lucas.com', [email], fail_silently=False)
