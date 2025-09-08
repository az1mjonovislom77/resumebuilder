from django.urls import path
from users import views
from users.views import (
    RegisterView,
    VerifyEmailView,
    EmailPageView,
    RegisterAPIView,
    LoginAPIView,
    VerifyEmailAPIView,
    LogoutAPIView,
)

app_name = "users"

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("logout/", views.logout_page, name="logout_page"),
    path("register/", RegisterView.as_view(), name="register_page"),
    path("email_page/", EmailPageView.as_view(), name="email_page"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),

    path("api/register/", RegisterAPIView.as_view(), name="api_register"),
    path("api/login/", LoginAPIView.as_view(), name="api_login"),
    path("api/verify-email/", VerifyEmailAPIView.as_view(), name="api_verify_email"),
    path("api/logout/", LogoutAPIView.as_view(), name="api_logout"),
]
