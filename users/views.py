import secrets
from django.core.mail import EmailMessage
from django.conf import settings
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, VerifyEmailSerializer
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
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                verification = serializer.save()
            except IntegrityError:
                return Response(
                    {"error": "This email is already registered."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            send_verification_email(verification.email, verification.code)
            return Response(
                {"message": "Verification code sent to your email."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class VerifyEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Email verified successfully! You can now log in."},
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
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
