import secrets
from rest_framework import serializers
from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password2", "phone_number"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Parollar bir xil emas!")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2", None)
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.verification_code = str(secrets.randbelow(1000000)).zfill(6)
        user.save()
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


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("verification_code")

        user = CustomUser.objects.filter(email=email, verification_code=code).first()
        if not user:
            raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri")

        return attrs
