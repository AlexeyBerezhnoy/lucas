from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.validators import validate_email
from account.validator import validate_name
from account.models import Moderator
from account.views import get_new_password
from account.views import send_message


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            self.stdout.write('Email:', ending=" ")
            email = input().lower()
            try:
                validate_email(email)
            except ValidationError:
                self.stderr.write("email невалиден")
            else:
                try:
                    Moderator.objects.get(email=email)
                except ObjectDoesNotExist:
                    break
                else:
                    self.stderr.write("email уже используется")

        while True:
            self.stdout.write('Фамилия:', ending=" ")
            last_name = input()
            try:
                validate_name(last_name)
            except ValidationError:
                self.stderr.write("Данные невалидны")
            else:
                break

        while True:
            self.stdout.write('Имя:', ending=" ")
            first_name = input()
            try:
                validate_name(first_name)
            except ValidationError:
                self.stderr.write("Данные невалидны")
            else:
                break

        while True:
            self.stdout.write('Отчество:', ending=" ")
            middle_name = input()
            try:
                validate_name(middle_name)
            except ValidationError:
                self.stderr.write("Данные невалидны")
            else:
                break

        Moderator.objects.create_moderator(email=email,
                                           first_name=first_name,
                                           middle_name=middle_name,
                                           last_name=last_name)

        moderator = Moderator.objects.get(email=email)
        password = get_new_password()
        moderator.set_password(password)
        moderator.save()

        subject = "Добро пожаловать"
        ctx = {'user': moderator, 'password': password}
        message = render_to_string('account/email/invite_moderator.html', ctx)
        send_message(moderator.email, subject, message)