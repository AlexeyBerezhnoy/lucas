from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView, DeletionMixin, CreateView

from account.models import MyUser, Expert
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


class SendEmailMixin:
    email_template_name = ''  # path to template for email message
    email_subject = ''
    email_context_data = {}
    from_email = 'admin@lucas.com'
    receivers = tuple()

    def get_email_context_data(self):
        return self.email_context_data

    def get_receivers(self):
        return self.receivers

    def render_email(self):
        return render_to_string(self.email_template_name, self.get_email_context_data())

    def send(self):
        send_mail(self.email_subject, self.render_email(), self.from_email, self.get_receivers, fail_silently=False)


# TODO: дай вьювам нормальные имена
@method_decorator(login_required, name='dispatch')
class ShowProfileView(FormView):
    model = MyUser
    success_url = reverse_lazy("account:cabinet")
    template_name = 'account/profile/show_profile.html'

    def get_form(self):
        if self.get_object().is_moderator:
            form = ModeratorForm
        else:
            form = ExpertForm
        return form(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(ShowProfileView, self).get_context_data(**kwargs)
        context['password_change_form'] = PasswordChangeForm()
        return context

    def get_initial(self):
        return self.model.objects.filter(email=self.get_object().email).values()[0]

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form=None):
        profile = MyUser.objects.filter(email=self.get_object().email)
        profile.update(**form.cleaned_data)
        messages.success(self.request, 'Информация изменена')
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form=None):
        messages.error(self.request, 'Форма невалидна')
        return render(self.request, self.template_name, {"form": form})


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


class ExpertList(ListView):
    queryset = Expert.objects.filter(is_expert=True)
    template_name = "account/experts/experts.html"


class CreateExpertView(CreateView, SendEmailMixin):
    model = Expert
    form_class = ExpertForm
    object = None
    password = None
    template_name = 'account/experts/new_expert.html'
    success_url = reverse_lazy('account:experts')

    email_subject = 'Добро пожаловать'
    email_template_name = 'account/email/invite_expert.html'
    to = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.password = get_new_password()
        self.object.set_password(self.password)
        self.object.save()
        messages.success(self.request, "Пользователь добавлен")

        self.send()

        return HttpResponseRedirect(self.success_url)

    def get_email_context_data(self):
        return {'user': self.object, 'password': self.password}

    def get_receivers(self):
        return tuple(self.object.email)


@method_decorator(is_moderator, name='dispatch')
class ExpertView(UpdateView, DeletionMixin):
    model = Expert
    form_class = ExpertForm
    template_name = 'account/experts/show_expert.html'
    success_url = reverse_lazy('account:experts')


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
