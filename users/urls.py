from django.urls import path
from .views import (
    RegisterAPIView,
    VerifyEmailAPIView,
    LoginAPIView,
    LogoutAPIView, ForgotPasswordAPIView, ResetPasswordAPIView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify_email"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
]
