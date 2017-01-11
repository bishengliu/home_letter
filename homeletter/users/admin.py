from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.


class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(User, UserAdmin)

fields = ('image_tag',)
readonly_fields = ('image_tag',)
