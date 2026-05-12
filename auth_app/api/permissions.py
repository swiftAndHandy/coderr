from rest_framework import permissions


class IsBusinessUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.profile.type == "business") or request.user.is_superuser