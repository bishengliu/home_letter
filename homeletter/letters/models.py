from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class LetterCategory(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='categories/', max_length=100, null=True, blank=True)
    date = models.DateField()
    in_use = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Letter(models.Model):
    category = models.ForeignKey(LetterCategory)
    name = models.CharField(max_length=250)
    file_path = models.FileField(upload_to='letters/', max_length=250, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    favorite = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
