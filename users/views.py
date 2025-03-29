from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from materials.models import Course
from .models import User, Payment, Subscription
from .permissions import IsProfileOwner
from .serializers import (
    UserSerializer,
    PaymentSerializer,
    UserDetailSerializer,
    RegisterSerializer,
)

import logging


logger = logging.getLogger(__name__)


# -- User ViewSet --
class UserViewSet(viewsets.ModelViewSet):
    """CRUD для пользователей (только авторизованные)."""

    queryset = User.objects.all().order_by("id")

    # Аутентификация и разрешения
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            if self.request.user == self.get_object():
                return UserDetailSerializer  # Полный доступ для владельца
        elif self.action == "create":
            return RegisterSerializer
        return UserSerializer  # Ограниченный доступ для чужого профиля и списка профилей

    def get_permissions(self):
        """Ограничиваем редактирование только владельцам"""
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsProfileOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        """Переопределяет создание пользователя для логгирования."""
        self.permission_classes = [AllowAny]
        response = super().create(request, *args, **kwargs)
        logger.info(
            "Пользователь с именем %s и email %s успешно создан." % (request.data["username"], request.data["email"])
        )
        return response

    def list(self, request, *args, **kwargs):
        """Переопределяет получение списка пользователей для логгирования."""
        self.permission_classes = [IsAuthenticated]
        response = super().list(request, *args, **kwargs)
        logger.info("Список пользователей успешно получен.")
        return response

    def retrieve(self, request, *args, **kwargs):
        """Переопределяет получение информации о пользователе для логгирования."""
        self.permission_classes = [IsAuthenticated]
        response = super().retrieve(request, *args, **kwargs)
        logger.info("Информация о пользователе с id %s успешно получена." % kwargs["pk"])
        return response

    def update(self, request, *args, **kwargs):
        """Переопределяет обновление информации о пользователе для логгирования."""
        self.permission_classes = [IsAuthenticated]
        response = super().update(request, *args, **kwargs)
        logger.info("Информация о пользователе с id %s успешно обновлена." % kwargs["pk"])
        return response

    def destroy(self, request, *args, **kwargs):
        """Переопределяет удаление пользователя для логгирования."""
        self.permission_classes = [IsAuthenticated]
        response = super().destroy(request, *args, **kwargs)
        logger.info("Пользователь с id %s успешно удален." % kwargs["pk"])
        return response


# -- Payment ViewSet --
class PaymentViewSet(viewsets.ModelViewSet):
    """Класс для представления оплат в API."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Фильтрация, поиск и сортировка
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Фильтрация по конкретным полям
    filterset_fields = ["user", "course", "lesson", "payment_method"]

    # Поля, по которым можно выполнять поиск (по частичному совпадению)
    search_fields = ["user__email", "course__name", "lesson__name"]

    # Поля, по которым можно сортировать (`ordering=-date` для сортировки по убыванию)
    ordering_fields = ["date", "amount"]


# -- Subscription ViewSet --
class SubscriptionAPIView(APIView):
    """API для управления подписками пользователей на курсы."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Переопределяет создание/удаление подписки и добавляет логгирование."""
        user = request.user
        course_id = request.data.get("course_id")

        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
            logger.info("Подписка на курс %s удалена пользователем %s", course_item, user)
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
            logger.info("Подписка на курс %s добавлена пользователем %s", course_item, user)

        return Response({"message": message})
