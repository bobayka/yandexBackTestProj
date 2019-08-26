import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

charOrDigValidate = RegexValidator(regex=r'^[\da-zA-Zа-яА-ЯёЁ\s]+$', flags=re.MULTILINE)


def validate_birthday(val):
    if val >= date.today():
        raise ValidationError('%s is greater then now time' % val)
