from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = "You do not have permission to access this object."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user_id", None) == request.user.id
