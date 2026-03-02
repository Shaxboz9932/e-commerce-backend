from django.urls import path
from . import views

urlpatterns = [
    path("", views.CartItemListOrCreateAPIView.as_view()),
    path("<int:pk>/", views.CartItemDeleteAPIView.as_view()),
    path("update/<int:pk>/", views.CartItemQuantityUpdateAPIView.as_view()),
]
