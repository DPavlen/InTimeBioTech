from typing import Dict

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from users.models import VerificationCode, MyUser
from api.v1.task import send_email_message


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

    def validate(self, data: Dict) -> Dict:
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

    def create(self, validated_data: Dict) -> VerificationCode:
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
