from django.db import models

from marketAnalysis import validators


class Import(models.Model):

    def __str__(self):
        return f'Import: {self.pk}'


# Create your models here.
class Citizen(models.Model):
    imports = models.ForeignKey(Import, on_delete=models.CASCADE, related_name='citizens')
    citizen_id = models.PositiveIntegerField()
    town = models.CharField(max_length=256, validators=[validators.charOrDigValidate])
    street = models.CharField(max_length=256, validators=[validators.charOrDigValidate])
    building = models.CharField(max_length=256, validators=[validators.charOrDigValidate])
    apartment = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=256)
    birth_date = models.DateField()
    gender = models.CharField(max_length=6, choices=(('male', 'male'), ('female', 'female')))
    relatives = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f'Import_id: {self.imports}, Citizen_id:{self.citizen_id}, name: {self.name}, relatives: {self.relatives}'
