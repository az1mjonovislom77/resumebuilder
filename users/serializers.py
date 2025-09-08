import secrets
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import CustomUser, EmailVerification


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone_number = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Parollar bir xil emas!")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2", None)

        code = str(secrets.randbelow(1000000)).zfill(6)

        verification = EmailVerification.objects.create(
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            password=make_password(password),  # hashed saqlash
            code=code,
        )

        # bu joyda email yuborishingiz mumkin: send_mail("Verification code", code, ...)
        return verification


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("verification_code")

        verification = EmailVerification.objects.filter(email=email, code=code).first()
        if not verification:
            raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri")
        if verification.is_expired():
            raise serializers.ValidationError("Tasdiqlash kodi muddati tugagan")

        return {"verification": verification}

    def create(self, validated_data):
        verification = validated_data["verification"]

        user = CustomUser.objects.create(
            email=verification.email,
            phone_number=verification.phone_number,
            first_name=verification.first_name,
            last_name=verification.last_name,
            password=verification.password,  # bu allaqachon hashed
            is_active=True,
        )

        verification.delete()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")

        if not user.check_password(password):
            raise serializers.ValidationError("Parol noto‘g‘ri")

        if not user.is_active:
            raise serializers.ValidationError("Email hali tasdiqlanmagan")

        return {"user": user}
