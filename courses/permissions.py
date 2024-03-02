from rest_framework import permissions


def user_can_access_product(user, product):
    return user in product.users_with_access


class IsProductOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user or request.user.is_staff
