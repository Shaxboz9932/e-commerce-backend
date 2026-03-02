from django.urls import path
from users.views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('get/', GetUserAPIView.as_view()),

    path("forgot/password/", RequestPasswordResetAPIView.as_view()),
    path("reset/password/", PasswordTokenCheckAPIView.as_view()),
    path("verify/email/", CheckEmailAPIView.as_view()),
]

