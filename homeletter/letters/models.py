from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from category.models import Category
from django.urls import reverse
from datetime import datetime
import os

"""
#/letters/2017/ABN_AMRO
def upload_path_handler():
    # return "letters/{year}/".format(year=str(datetime.now().year))
    return os.path.join("letters/", str(datetime.now().year), "/")
"""

class Letter(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=250, unique=True)
    file = models.FileField(upload_to="letters/", max_length=250, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    favorite = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('letters:index')

    class Meta:
        verbose_name_plural = "letters"
