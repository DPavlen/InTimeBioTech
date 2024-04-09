from django.contrib import admin

from .models import MyUser


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

    list_display = ("id", "email", "last_name", "first_name", "phone_number")
    search_fields = ("email", "last_name", "first_name", "phone_number")