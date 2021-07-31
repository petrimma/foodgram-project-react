from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class RecipePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS 
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS 
                or (request.method == "POST" and request.user.is_authenticated)
                or obj.author == request.user
                or request.user.is_staff)


class SubscribePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (view.action == "list"
                and (obj.user == request.user or request.user.is_staff)
                or request.user.is_authenticated)
                