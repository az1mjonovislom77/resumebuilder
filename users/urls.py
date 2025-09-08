from django.urls import path
from .views import (
    RegisterAPIView,
    EmailPageAPIView,
    VerifyEmailAPIView,
    LoginAPIView,
    LogoutAPIView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("email/", EmailPageAPIView.as_view(), name="email_page"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify_email"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
