from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from djoser.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import MyUser, VerificationCode
from api.v1.task import send_email_message


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор работы с пользователями.
    Сериализатор, расширяющий базовый сериализатор пользователя,
    для обработки дополнительных полей.
    Attributes:
        - Meta: Класс метаданных для определения модели и полей сериализатора.
    """

    class Meta:
        model = MyUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "surname",
            "sex",
            "phone_number",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "surname": {"required": False},
            "sex": {"required": True},
            "phone_number": {"required": False},
            "is_active": {"required": False, "read_only": True},
        }

    def create(self, validated_data):
        user = MyUser(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomUserReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения пользователей.
    Сериализатор, предназначенный только для чтения данных пользователя.
    Attributes:
        - Meta: Класс метаданных для определения модели и полей сериализатора.
    """

    class Meta:
        model = MyUser
        fields = ("id", "first_name", "last_name")


class VerificationCodeSerializer(ModelSerializer):
    """
    Сериализатор для модели VerificationCode.
    Проверяет корректность электронной почты пользователя
    и создает новый OTP-код для верификации.
    Attributes:
        model (Model): Модель VerificationCode.
        fields (str): Список полей для сериализации.
        read_only_fields (tuple): Список полей только для чтения.

    Methods:
        validate(data): Проверяет корректность электронной почты пользователя.
        create(validated_data): Создает новый OTP-код для верификации.
    """

    class Meta:
        model = VerificationCode
        fields = '__all__'
        read_only_fields = ('otp_code', 'expiration', 'used')

    def validate(self, data):
        """
        Проверяет валидность данных, включая электронную почту и ее наличие в базе данных.
        Args: data (dict): Словарь с данными для валидации.
        Returns: dict: Валидные данные.
        Raises: Проверка @ в БД и ошибка если ее нет.
        """

        email = data.get('email')
        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))

        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Пользователь с указанной электронной почтой не найден.")

        return data

    def create(self, validated_data):
        """
        Создает новый OTP-код для верификации.
        Args: validated_data (dict): Валидированные данные.
        Returns:
            VerificationCode: Созданный объект OTP-кода верификации.
        """

        email = validated_data['email']
        user_otp = VerificationCode.objects.create_otp_code(email)
        # user_otp = VerificationCode.objects.create_otp_code(**validated_data)
        send_email_message.delay(user_otp.email, user_otp.otp_code)
        return user_otp


class AuthOTPCodeSerializer(serializers.Serializer):
    """
    Сериализатор для проверки OTP-кода аутентификации.
    Attributes:
        - email (EmailField): Поле для адреса электронной почты пользователя.
        - otp_code (IntegerField): Поле для OTP-кода, введенного пользователем.
    Meta: Класс метаданных для определения модели и полей сериализатора.
    """

    email = serializers.EmailField()
    otp_code = serializers.IntegerField()

    class Meta:
        model = VerificationCode
        fields = '__all__'
        read_only_fields = ('otp_code', 'expiration', 'used')