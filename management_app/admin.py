from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from management_app.models import CustomUser


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)  # registering the usermodel with the admin site to connect it with the db and further access.