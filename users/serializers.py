from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ["id", 'username', 'first_name', 'last_name', 'email', 'created', 'updated']

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=200, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'last_name', 'first_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol 8tadan kam bo'lmasligi kerak")
        return value

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


