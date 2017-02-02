from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='categories/', max_length=100, null=True, blank=True)
    date = models.DateField()
    in_use = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

