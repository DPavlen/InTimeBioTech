from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants.users import (
    EMAIL_LENGTH,
    NAME_LENGTH,
    PHONE_NUMBER_LENGTH,
    ROLE_LENGTH,
    SEX_LENGTH
)


class UserManager(BaseUserManager):
    """
    Менеджер пользователей.
    Этот менеджер обеспечивает создание и управление пользователями в системе.
    Methods:
        - _create_user(email, password, **extra_fields): Создает и сохраняет
        пользователя с заданным email и паролем.
        - create_user(email, password=None, **extra_fields): Создает и
        сохраняет обычного пользователя.
        - create_superuser(email, password, **extra_fields): Создает и
        сохраняет суперпользователя.
    Attributes:
        - use_in_migrations: Флаг, указывающий, что этот менеджер
        используется в миграциях.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с заданным email и паролем.
        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param extra_fields: Дополнительные поля пользователя.
        :return: Созданный пользователь.
        """
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя.
        :param email: Email суперпользователя.
        :param password: Пароль суперпользователя.
        :param extra_fields: Дополнительные поля суперпользователя.
        :return: Созданный суперпользователь.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    """
    Пользователь.
    Модель пользователя для авторизации и управления правами.
    Attributes:
        - USER: Константа для роли обычного пользователя.
        - ADMIN: Константа для роли администратора.
        - ROLES: Кортеж с выбором ролей пользователя.
        - SEX_CHOICES: Кортеж с выбором пола пользователя.
        - USERNAME_FIELD: Поле для использования в качестве имени
        пользователя при аутентификации.
        - REQUIRED_FIELDS: Обязательные поля при создании пользователя.
        - objects: Менеджер для работы с пользователями.
    """

    USER = "user"
    ADMIN = "admin"

    ROLES = (
        (USER, USER),
        (ADMIN, ADMIN)
    )

    SEX_CHOICES = (
        ("М", "Male"),
        ("Ж", "Female")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    first_name = models.CharField(
        "Имя",
        max_length=NAME_LENGTH
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=NAME_LENGTH
    )
    surname = models.CharField(
        "Отчество",
        null=True,
        blank=True,
        max_length=NAME_LENGTH
    )
    sex = models.CharField(
        "Пол",
        max_length=SEX_LENGTH,
        choices=SEX_CHOICES,
        null=True,
        blank=True,
        help_text="Выберите пол",
    )
    email = models.EmailField(
        "Электронная почта",
        max_length=EMAIL_LENGTH,
        unique=True,
        help_text="Введите адрес электронной почты",
    )
    phone_number = models.CharField(
        "Номер телефона",
        max_length=PHONE_NUMBER_LENGTH,
        blank=True,
        unique=True,
        null=True,
        # validators=
        help_text="Введите номер телефона",
    )
    role = models.CharField(
        "Роль",
        max_length=ROLE_LENGTH,
        choices=ROLES,
        default=USER,
        blank=True,
        help_text="Роль пользователя"
    )

    username: None = None

    @property
    def is_admin(self):
        """
        Проверяет, является ли пользователь администратором.
        :return: True, если пользователь является администратором,
        в противном случае - False.
        """
        return self.role == self.ADMIN

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Возвращает строковое представление пользователя.
        :return: Строковое представление в формате "Имя Фамилия @".
        """
        return f"{self.first_name} {self.last_name} {self.email}"






