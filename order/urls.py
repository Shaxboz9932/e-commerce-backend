from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("", views.OrderListOrCreateAPIView.as_view()),

    path("process/<int:pk>/", views.payment_process, name="process"),
    path("completed/", views.payment_completed, name="completed"),
    path("canceled/", views.payment_canceled, name="canceled")

]
