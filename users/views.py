import secrets
from django.core.mail import EmailMessage
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import load_strategy, load_backend
from .serializers import RegisterSerializer, LoginSerializer, VerifyEmailSerializer, ResetPasswordSerializer, \
    ForgotPasswordSerializer
from .permissions import IsAuthenticated


def generate_verification_code():
    return str(secrets.randbelow(1000000)).zfill(6)


def send_verification_email(email, code):
    mail_subject = "Your Registration Verification Code"
    message = f"Hello {email},\n\nYour verification code is: {code}"
    email_obj = EmailMessage(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email_obj.send()


@extend_schema(tags=['Auth'])
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            verification = serializer.save()
            return Response({
                "message": "Tasdiqlash kodi sizning emailingizga yuborildi. Iltimos, kodni kiriting va ro‘yxatdan o‘ting."
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class VerifyEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Email verified successfully! You can now log in"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            if not user:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
class ForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset code sent to your email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class ResetPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class SocialLoginURLsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from django.urls import reverse
        return Response({
            "google_login_url": request.build_absolute_uri(
                reverse('social:begin', kwargs={'backend': 'google-oauth2'})),
            "github_login_url": request.build_absolute_uri(reverse('social:begin', kwargs={'backend': 'github'})),
        })


@extend_schema(tags=['Auth'])
class SocialLoginCompleteAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, backend, *args, **kwargs):
        strategy = load_strategy(request)
        social_backend = load_backend(strategy, backend, None)
        try:
            user = social_backend.do_auth(request.GET.get('code'), request=request)
            if user and user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
