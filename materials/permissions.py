from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name="Moderator").exists()


class IsOwnerOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Moderator").exists():
            return request.method in ("GET", "PUT", "PATCH")
        if hasattr(obj, "user") and obj.user == request.user:
            return True
        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user") and obj.user == request.user:
            return True
        return False
