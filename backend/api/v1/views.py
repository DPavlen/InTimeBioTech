from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from api.v1.serializers import VerificationCodeSerializer
from users.models import VerificationCode


class VerificationCodeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    queryset = VerificationCode.objects.all()
    serializer_class = VerificationCodeSerializer
    # permissions = [IsAuthenticated]


