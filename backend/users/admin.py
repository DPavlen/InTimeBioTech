from django.contrib import admin

from .models import MyUser, VerificationCode


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели User.
    Параметры:
        - list_display: Поля, которые будут отображаться в
        списке пользователей.
        - search_fields: Поля, по которым можно выполнять поиск пользователей.
    Модель:
        - MyUser.
    """

    list_display = ("id", "email", "last_name", "first_name", "role")
    search_fields = ("email", "last_name", "first_name", "role")


@admin.register(VerificationCode)
class VerificationCode(admin.ModelAdmin):
    """
    Класс администратора для модели class VerificationCode.
    Параметры:
        - list_display: Поля, которые будут отображаться в
        списке пользователей.
        - search_fields: Поля, по которым можно выполнять поиск пользователей.
    Модель:
        - VerificationCode.
    """

    list_display = ("id", "email", "otp_code", "expiration", "used")
    search_fields = ("email", "otp_code", "expiration", "used")