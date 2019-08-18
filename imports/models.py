from enum import Enum

from django.db import models


class GenderChoice(Enum):
    male = 'male'
    female = 'female'


# Create your models here.
class Citizen(models.Model):
    citizen_id = models.BigIntegerField(primary_key=True)
    town = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    building = models.CharField(max_length=200)
    apartment = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=200)
    birth_date = models.DateField()
    gender = models.CharField(max_length=6,
                              choices=[(tag, tag.value()) for tag in GenderChoice])
    import_id = models.BigIntegerField()


class Relatives(models.Model):
    relatives_id = models.BigIntegerField(primary_key=True)
    citizen = models.ForeignKey(Citizen)
