from django.urls import include, path
from rest_framework import routers

from api.v1.views import VerificationCodeViewSet

app_name = "api.v1"

router = routers.DefaultRouter()


router.register(r"verification_codes", VerificationCodeViewSet, "verification_codes")


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]


