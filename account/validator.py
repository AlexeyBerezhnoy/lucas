import re
from django.core.exceptions import ValidationError


def validate_name(value):
    if not re.match(r'^[А-Я][а-я]*(\-[а-я]*)*$', value):
        raise ValidationError('Поддерживаются только русские буквы\
                              и тире. Перая буква Должна быть заглавной')


def validate_profession(value):
    if not re.match(r'^[А-Яа-я]+([\s\-][А-Яа-я]+)*$', value):
        raise ValidationError('Поддерживаются только русские буквы тире и пробел')


def validate_experience(value):
    if not re.match(r'^(0|[1-9][0-9]?)$', str(value)):
        raise ValidationError("Поддерживаются только целые числа от 0 до 99")