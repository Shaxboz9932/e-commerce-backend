from django.urls import path
from .views import *

urlpatterns = [
    path('', GetProductsAPIView.as_view()),
    path('<int:pk>/', GetProductAPIView.as_view()),

    path('get/category/', GetCategory.as_view()),
    path('get/brand/', GetBrand.as_view()),
]