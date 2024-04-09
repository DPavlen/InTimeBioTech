from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import MyUser


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
            "phone_number": {"required": False},
            "is_active": {"required": False, "read_only": True},
        }

    def create(self, validated_data):
        user = MyUser(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        if "telegram_id" in validated_data:
            user.telegram = validated_data["telegram"]
        if "phone_number" in validated_data:
            user.phone_number = validated_data["phone_number"]

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
