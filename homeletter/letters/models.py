from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class LetterCategory(models.Model):
    name = models.CharField(max_length=100),
    logo = models.ImageField(upload_to='categories/', max_length=100, null=True, blank=True),
    date = models.DateField(),
    in_use = models.BooleanField(default=False),
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    note = models.TextField(null=True, blank=True)


class Letter(models.Model):
    category_id = models.ForeignKey(LetterCategory),
    name = models.CharField(max_length=250),
    date = models.DateField(),
    favorite = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)]),
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    note = models.TextField(null=True, blank=True)
