from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import FormView, UpdateView, DeletionMixin, CreateView

from account.models import MyUser, Expert
from account.forms import LoginForm, ExpertForm, ModeratorForm, PasswordChangeForm, ForgotPasswordForm
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
        send_mail(self.email_subject, self.render_email(), self.from_email, self.get_receivers(), fail_silently=False)


# TODO: дай вьювам нормальные имена
@method_decorator(login_required, name='dispatch')
class ShowProfileView(FormView):
    model = MyUser
    success_url = reverse_lazy("account:cabinet")
    template_name = 'account/profile/show_profile.html'

    def get_form(self, form_class=None):
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

    def get_object(self):
        return self.request.user

    def form_valid(self, form=None):
        profile = MyUser.objects.filter(email=self.get_object().email)
        profile.update(**form.cleaned_data)
        messages.success(self.request, 'Информация изменена')
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form=None):
        messages.error(self.request, 'Форма невалидна')
        return render(self.request, self.template_name, {"form": form})


class ChangePasswordView(FormView):
    http_method_names = ['post']
    form_class = PasswordChangeForm
    success_url = reverse_lazy('account:cabinet')

    def form_valid(self, form):
        user = self.get_object()

        logout(self.request)

        user.set_password(form.cleaned_data['new_password'])
        user.save()

        user = authenticate(email=user.email, password=form.cleaned_data['new_password'])
        login(self.request, user)

        messages.success(self.request, 'Пароль успешно изменён')
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        print(form)
        messages.error(self.request, 'Некорректно заполненая форма')
        return HttpResponseRedirect(self.success_url)

    def get_object(self):
        return self.request.user


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
        return (self.object.email, )


@method_decorator(is_moderator, name='dispatch')
class ExpertView(UpdateView, DeletionMixin):
    model = Expert
    form_class = ExpertForm
    template_name = 'account/experts/show_expert.html'
    success_url = reverse_lazy('account:experts')


class ToggleActivityExpertView(UpdateView):
    http_method_names = ['get']
    model = Expert
    success_url = reverse_lazy('account:experts')

    def get(self, request, *args, **kwargs):
        if self.object.is_active:
            self.object.is_active = False
            messages.success(self.request, "Пользователь заморожен")
        else:
            self.object.is_active = True
            messages.success(self.request, "Пользователь разморожен")
        self.object.save()
        HttpResponseRedirect(self.success_url)


class ResetPasswordView(UpdateView, SendEmailMixin):
    http_method_names = ['get']
    model = Expert
    success_url = reverse_lazy('account:experts')

    email_template_name = 'account/email/new_password.html'
    email_subject = 'Пароль обновлен'
    from_email = 'admin@lucas.com'

    password = None

    def get(self, request, *args, **kwargs):
        self.password = get_new_password()
        expert = self.get_object()
        expert.set_password(self.password)
        expert.save()

        self.send()
        return HttpResponseRedirect(self.success_url)

    def get_email_context_data(self):
        return {'user': self.object, 'password': self.password}

    def get_receivers(self):
        return (self.object.email, )


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = reverse_lazy("account:cabinet")

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        return HttpResponseRedirect(self.success_url)


class ForgotPasswordView(FormView, SendEmailMixin):
    form_class = ForgotPasswordForm
    template_name = 'account/forgot_password.html'
    success_url = reverse_lazy('account:login')

    email_template_name = 'account/email/new_password.html'
    email_subject = 'Пароль обновлен'

    object = None
    password = None

    def form_valid(self, form):
        self.object = form.get_user()
        self.password = get_new_password()
        self.object.set_password(self.password)
        self.object.save()

        messages.success(self.request, 'пароль обновлен')
        self.send()

        return HttpResponseRedirect(self.success_url)

    def get_receivers(self):
        return (self.object.email, )

    def get_email_context_data(self):
        return {'user': self.object, 'password': self.password}


def get_new_password(length=4):
    return MyUser.objects.make_random_password(length=length)
