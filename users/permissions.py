from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """Разрешает владельцу полный доступ к объекту."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.owner == request.user


class IsModerator(BasePermission):
    """Разрешает модератору все операции кроме create и destroy."""

    def has_permission(self, request, view):
        is_moderator = request.user.groups.filter(name="Модераторы").exists()
        return is_moderator and view.action not in ["create", "destroy"]

    def has_object_permission(self, request, view, obj):
        """Модератор может просматривать и редактировать объект."""
        return request.user.groups.filter(name="Модераторы").exists()


class DenyAll(BasePermission):
    """Полностью запрещает доступ."""

    def has_permission(self, request, view):
        return False


class IsProfileOwner(BasePermission):
    """Разрешает изменение только владельцу, но просмотр доступен всем авторизованным пользователям."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True  # Разрешаем просмотр профилей всем авторизованным
        return obj == request.user  # Разрешаем изменение только владельцу
