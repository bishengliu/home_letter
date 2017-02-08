from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.ImageField(upload_to='category/', max_length=100, null=True, blank=True)
    date = models.DateField()
    in_use = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category:index')

    class Meta:
        verbose_name_plural = "Categories"
