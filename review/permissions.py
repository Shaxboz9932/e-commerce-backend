from rest_framework.permissions import BasePermission

from review.models import Review


from rest_framework.permissions import BasePermission

class IsYourReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Faqat egasi o‘zgartiradi / o‘chira oladi
        return obj.user == request.user

