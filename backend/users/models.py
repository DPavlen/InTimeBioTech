from random import randint
from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from backend import settings
from core.constants.users import (
    EMAIL_LENGTH,
    NAME_LENGTH,
    PHONE_NUMBER_LENGTH,
    ROLE_LENGTH,
    SEX_LENGTH
)

from core.validators import validate_phone_number


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


class VerificationOtpCodeManager(models.Manager):
    """
    Менеджер для управления OTP-кодами верификации.
    Позволяет создавать новые OTP-коды,
    проверять их валидность и управлять их сроком действия.
    """

    @staticmethod
    def create_new_otp_code():
        """
        Создает новый OTP-код.
        Returns:
            int: Сгенерированный рандомный 6-ти значный OTP-код.
        """
        return randint(100000, 999999)

    def otp_code_validation(self, email, otp_code):
        """
        Проверяет валидность OTP-кода для указанного адреса электронной почты.
        Args:
            email (str): Адрес электронной почты пользователя.
            otp_code (int): Проверяемый OTP-код.
        Returns:
             bool: True, если OTP-код валиден и
             не использован или не истек, в противном случае False.
        """

        otp_code = self.filter(
            otp_code=otp_code,
            email=email,
            used=False,
            expiration__gt=timezone.now() - timedelta(
                minutes=settings.OTP_CODE_EXPIRATION_TIME))
        if not otp_code:
            return False
        otp_code.update(used=True)
        return True

    def create_otp_code(self, email):
        """
        Создает новый OTP-код для указанного адреса электронной почты
        и удаляет использованные или просроченные коды.
        Parameters:
            email (str): Адрес электронной почты пользователя.
        Returns:
            VerificationCode: Созданный объект кода верификации OTP.
        """

        self.filter(email=email, used=True).delete()
        self.filter(email=email,
                    expiration__lt=timezone.now() - timedelta(minutes=settings.OTP_CODE_EXPIRATION_TIME)).delete()
        # 90 минут
        valid_codes = self.filter(
            email=email, used=False,
            expiration__gt=timezone.now() - timedelta(minutes=settings.OTP_CODE_EXPIRATION_TIME))
        if valid_codes:
            # Если есть неиспользованный код, обновляем его срок действия
            valid_code = valid_codes.first()
            valid_codes.update(expiration=timezone.now() + timedelta(minutes=settings.OTP_CODE_EXPIRATION_TIME))
            return valid_code
        else:
            # Если неиспользованный код не найден, создаем новый
            otp_code = self.create_new_otp_code()
            verification_code = self.create(
                email=email, otp_code=otp_code,
                expiration=timezone.now() + timedelta(minutes=settings.OTP_CODE_EXPIRATION_TIME))
            return verification_code


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
        validators=[validate_phone_number],
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
        return f"{self.first_name} {self.last_name} "


class VerificationCode(models.Model):
    """
    Модель для хранения информации о кодах верификации по электронной почте.
    Attributes:
        email (str): Адрес электронной почты пользователя.
        otp_code (int): OTP-код верификации.
        expiration (datetime): Время истечения срока действия кода верификации.
        used (bool): Флаг указывает, использован ли код верификации.
        objects (VerificationOtpCodeManager):
            Менеджер для работы с объектами модели VerificationCode.
    """

    email = models.EmailField(
        "Электронная почта",
        max_length=EMAIL_LENGTH,
        unique=True,
        help_text="Введите адрес электронной почты",
    )
    otp_code = models.IntegerField()
    expiration = models.DateTimeField()
    used = models.BooleanField(default=False)

    objects = VerificationOtpCodeManager()

    class Meta:
        verbose_name = "Код верификации"
        verbose_name_plural = "Коды верификации"
        unique_together = ['email', 'otp_code']

    def __str__(self):
        """
        Возвращает строковое представление пользователя.
        :return: Строковое представление в формате "email" и "otp_code".
        """
        return f"{self.otp_code}"