from rest_framework.permissions import BasePermission


class IsAdminForPost(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(request.user and request.user.is_staff)
        return True

class IsAdminForPatch(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PATCH':
            return bool(request.user and request.user.is_staff)
        return True

class IsAdminForDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return bool(request.user and request.user.is_staff)
        return True