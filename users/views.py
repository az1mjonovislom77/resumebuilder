import secrets
from django.core.mail import EmailMessage
from django.conf import settings
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, VerifyEmailSerializer
from .permissions import IsAuthenticated



def generate_verification_code():
    return str(secrets.randbelow(1000000)).zfill(6)


def send_verification_email(user):
    mail_subject = "Your Registration Verification Code"
    message = f"Hello {user.email},\n\nYour verification code is: {user.verification_code}"
    email = EmailMessage(
        mail_subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.send()


@extend_schema(tags=['Auth'])
class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.verification_code = generate_verification_code()
            user.save()
            send_verification_email(user)
            return Response(
                {"message": "User registered successfully. Check your email for verification."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Auth'])
class EmailPageAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email query param required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            return Response(
                {
                    "user_email": user.email,
                    "verification_code": user.verification_code,
                },
                status=status.HTTP_200_OK,
            )
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=['Auth'])
class VerifyEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = serializer.validated_data["verification_code"]

            try:
                user = CustomUser.objects.get(email=email, verification_code=code)
                user.is_active = True
                user.verification_code = ""
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"message": "Invalid verification code!"}, status=status.HTTP_400_BAD_REQUEST)

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
