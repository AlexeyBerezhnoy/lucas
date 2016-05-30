import re
from django.core.exceptions import ValidationError


def validate_quality_id(value):
    if not re.match(r'^(0|[1-9][0-9]*)$', str(value)):
        raise ValidationError("Поддерживаются только целые числа от 0 до 99")
    return 1


def validate_point(value):
    if not re.match(r'^([1-9])$', str(value)):
        print(str(value))
        raise ValidationError("Поддерживаются только целые числа от 1 до 10")
    return 1
