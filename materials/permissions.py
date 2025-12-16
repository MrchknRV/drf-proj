from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderator").exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class IsOwnerOrModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.groups.filter(name="Moderator").exists() or
            (hasattr(obj, 'owner') and obj.owner == request.user) or
            (hasattr(obj, 'user') and obj.user == request.user)
        )


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return hasattr(obj, 'owner') and obj.owner == request.user or \
               hasattr(obj, 'user') and obj.user == request.user
