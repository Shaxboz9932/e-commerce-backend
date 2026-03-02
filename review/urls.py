from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewListorCreateAPIView.as_view()),
    path("get/<int:pk>/", views.ReviewUpdateOrDeleteAPIView.as_view()),

    path("product/<int:pk>/", views.GetReviewsByProductId.as_view()),
]
