from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwner, IsModerator


class LessonPermissionMixin:
    """Миксин для настройки прав доступа в уроках."""

    def get_permissions(self):
        """Настраиваем права доступа для владельцев и модераторов."""

        if self.request.method in ["POST", "DELETE"]:
            self.permission_classes = [IsAuthenticated, IsOwner]  # Только владелец может создавать и удалять
        elif self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]  # Владелец и модератор могут редактировать
        else:  # Для "GET"
            self.permission_classes = [IsAuthenticated]  # Любой авторизованный пользователь может просматривать

        return [permission() for permission in self.permission_classes]
