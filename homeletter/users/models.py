from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class User(AbstractUser):
    def __str__(self):
        return self.username


# extend the user model using one-to-one link
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='users/', max_length=100, null=True, blank=True)

    # display photo in the admin
    def photo_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % self.photo)

    photo_tag.short_description = _('My Photo')

    # hook with User model
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #    if created:
    #        Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #   instance.profile.save()

