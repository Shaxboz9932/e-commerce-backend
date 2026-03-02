from django.urls import path
from . import views

urlpatterns = [
    path("", views.WishListOrCreateAPIView.as_view()),
    path("delete/<int:pk>/", views.WishlistItemDelete.as_view()),
]
