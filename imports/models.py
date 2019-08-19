from django.db import models

from imports import validators


class Import(models.Model):
    def __str__(self):
        return f'Import id: {self.pk}'


# Create your models here.
class Citizen(models.Model):
    import_id = models.ForeignKey(Import, on_delete=models.CASCADE)
    citizen_id = models.PositiveIntegerField()
    town = models.CharField(max_length=256, validators=[validators.charOrDigValidate])
    street = models.CharField(max_length=256, validators=[validators.charOrDigValidate])
    building = models.CharField(max_length=256, validators=[validators.charOrDigValidate])
    apartment = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=256)
    birth_date = models.DateField(validators=[validators.validate_birthday])
    gender = models.CharField(max_length=6, choices=(('male', 'male'), ('female', 'female')))

    def __str__(self):
        return f'Import_id: {self.import_id}, Citizen_id:{self.citizen_id}'


class Relatives(models.Model):
    relatives_id = models.BigIntegerField(primary_key=True)
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)

    def __str__(self):
        return f'Relatives_id: {self.relatives_id}'
