from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

from users.models import MyUser, VerificationCode
from users.serializers import CustomUserSerializer, VerificationCodeSerializer, AuthOTPCodeSerializer


class CustomUserViewSet(UserViewSet):
    """
    Кастомный ViewSet для работы с пользователями.
    Этот ViewSet предоставляет эндпоинты для управления пользователями,
    включая активацию.
    Attributes:
        - queryset: Запрос, возвращающий все объекты User.
        - serializer_class: Сериализатор, используемый для преобразования
        данных пользователя.
    Permissions:
        - permission_classes: Список классов разрешений для ViewSet. Здесь
        установлен AllowAny для открытого доступа.
    """

    queryset = MyUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self) -> Tuple:
        """
        Возвращает соответствующий сериализатор в зависимости от действия.
        """
        if self.action == "list":
            return (IsAdminUser(),)
        return (AllowAny(),)

    @action(detail=False, methods=['post'])
    def verification_code(self, request):
        """
        Верификация пользователя.
        """
        serializer = VerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

    @action(detail=False, methods=['post'])
    def auth_otp_code(self, request):
        """
        Проверяет OTP-код и авторизует пользователя.
        Parameters:
        request (Request): Запрос, содержащий данные OTP-кода.
        Returns:
        Response: Ответ с результатом авторизации. и получением токена.
        Raises:
        ValidationError: Если данные OTP-кода некорректны.
        """

        serializer = AuthOTPCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        otp_code = serializer.validated_data.get('otp_code')

        try:
            verification_code = VerificationCode.objects.get(
                email=email, otp_code=otp_code, used=False)
            verification_code.used = True
            verification_code.save()
            user = MyUser.objects.get(email=email)
            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "message": "Вы успешно авторизовались!",
                },
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(
                "OTP-код неверен или срок его действия истек",
                status=status.HTTP_400_BAD_REQUEST
            )
            