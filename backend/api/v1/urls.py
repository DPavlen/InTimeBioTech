from django.urls import include, path
from rest_framework import routers

from users.views import CustomUserViewSet

app_name = "api.v1"

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')


urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include("djoser.urls")),
    path("v1/auth/", include("djoser.urls.authtoken")),
    # path("v1/users/verification_code/", CustomUserViewSet.as_view(
    #     {'post': 'verification_code'}), name='verification_code'),
    # path('v1/auth_otp_code/', CustomUserViewSet.as_view(
    #     {'post': 'auth_otp_code'}), name='auth-otp-code'),

]


