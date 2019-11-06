from rest_framework import permissions


class IsTeacher(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if is_authenticated and request.method not in permissions.SAFE_METHODS:
            return request.user.profile.is_teacher
        return False
