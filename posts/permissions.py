from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение на изменение только для автора объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS запросы для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем запись только автору объекта
        return obj.author == request.user 