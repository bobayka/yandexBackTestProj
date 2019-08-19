import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

charOrDigValidate = RegexValidator(regex=r'[\d\w]+', flags=re.MULTILINE)


def validate_birthday(val):
    if val >= date.today():
        raise ValidationError('%s is less then now time' % val)


def validate_gender(val):
    if val not in ['male', 'female']:
        raise ValidationError('error in gender: %s' % val)
