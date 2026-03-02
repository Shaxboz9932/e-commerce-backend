from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
import random
from users.models import User
from users.serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        email = request.data.get("email")
        serializer = self.serializer_class(data=request.data)
        user_exist = User.objects.filter(email=email)
        if user_exist.exists():
            return Response({"detail": "Bu Email avval ro'yxatdan o'tgan"}, status=400)

        if serializer.is_valid():
            user = serializer.save()

            code = str(random.randint(100000, 999999))
            cache.set(f"otp_{email}", code, 180)

            send_mail(
                'Emailni tasdiqlash',
                f'Emailni tasdiqlash kodi: {code}',
                'admin@sayt.uz',
                [user.email],
                fail_silently=False,
            )

            return Response({"detail": "Emailni tasdiqlang"}, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckEmailAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get('code')

        true_code = cache.get(f"otp_{email}")

        if true_code and str(true_code) == str(code):
            try:
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
                cache.delete(f"otp_{email}")
                return Response({"detail": "Tabriklaymiz siz to'liq ruxatdan o'tdingiz"}, status=200)
            except User.DoesNotExist:
                return Response({"detail": "Fodalanuvchi topilmadi"}, status=404)
        else:
            return Response({"detail": "Kod xato yoki muddati tugagan"}, status=400)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh = request.data['refresh']
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({
                'detail': "Logout successful"
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({
                'error': "Invalid refresh token"
            }, status=status.HTTP_400_BAD_REQUEST)

class GetUserAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class RequestPasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.id)) #1 => b"1" => MT=
            token = PasswordResetTokenGenerator().make_token(user)

            reset_link = f"http://localhost:3000/reset-password/{uidb64}/{token}/"

            send_mail(
                "Parolni qayta tiklash",
                f"Parolni tiklash: {reset_link}",
                "from@example.com",
                ["to@example.com"],
                fail_silently=False,
            )
            return Response({"detail": "Emailga xabar yuborildi..."}, status=200)
        else:
            return Response({"detail": "Email mavjud emas..."}, status=404)

class PasswordTokenCheckAPIView(APIView):
    def post(self, request):
        try:
            uidb64 = request.data.get("uidb64")
            token = request.data.get("token")

            id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"detail": "Token yaroqsiz yoki muddati o'tgan..."}, status=400)

            new_password = request.data.get("password")
            user.set_password(new_password)
            user.save()

            return Response({"detail": "Parol muvaffaqiyatli o'zgartirildi..."}, status=200)
        except Exception as e:
            return Response({"deatil": "Nimadir xato ketdi..."}, status=400)














