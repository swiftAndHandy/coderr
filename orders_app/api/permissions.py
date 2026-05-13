from rest_framework import permissions


class IsContractedOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated and request.user == obj.business_user)
                or request.user.is_staff)