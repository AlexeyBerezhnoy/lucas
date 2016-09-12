from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from account.validator import validate_name
from getpass import getpass
from account.models import Moderator


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

        while True:
            self.stdout.write('Пароль:', ending=" ")
            password = getpass()
            try:
                validate_password(password)
            except ValidationError:
                self.stderr.write("Невозможно использовать как пароль")
            else:
                break

        while True:
            self.stdout.write('Повторите пароль:', ending=" ")
            confirm_password = getpass()
            if confirm_password != password:
                self.stderr.write("Неверное подтверждение пароля")
            else:
                break

        Moderator.objects.create_moderator(email=email,
                                           first_name=first_name,
                                           middle_name=middle_name,
                                           last_name=last_name,
                                           password=password)