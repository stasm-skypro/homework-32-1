from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User, Payment
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
        return (
            UserSerializer  # Ограниченный доступ для чужого профиля и списка профилей
        )

    def get_permissions(self):
        """Ограничиваем редактирование только владельцам"""
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsProfileOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        """Переопределение метода create для регистрации пользователей. В метод добавлены разрешения и логгер."""
        self.permission_classes = [AllowAny]
        response = super().create(request, *args, **kwargs)
        logger.info(
            "Пользователь с именем %s и email %s успешно создан."
            % (request.data["username"], request.data["email"])
        )
        return response

    def list(self, request, *args, **kwargs):
        """Переопределение метода list для вывода списка пользователей. В метод добавлены разрешения и логгер."""
        self.permission_classes = [IsAuthenticated]
        response = super().list(request, *args, **kwargs)
        logger.info("Список пользователей успешно получен.")
        return response

    def retrieve(self, request, *args, **kwargs):
        """Переопределение метода retrieve для вывода информации о пользователе. В метод добавлены разрешения и логгер."""
        self.permission_classes = [IsAuthenticated]
        response = super().retrieve(request, *args, **kwargs)
        logger.info(
            "Информация о пользователе с id %s успешно получена." % kwargs["pk"]
        )
        return response

    def update(self, request, *args, **kwargs):
        """Переопределение метода update для редактирования информации о пользователе. В метод добавлены разрешения и логгер."""
        self.permission_classes = [IsAuthenticated]
        response = super().update(request, *args, **kwargs)
        logger.info(
            "Информация о пользователе с id %s успешно обновлена." % kwargs["pk"]
        )
        return response

    def destroy(self, request, *args, **kwargs):
        """Переопределение метода destroy для удаления пользователя. В метод добавлены разрешения и логгер."""
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
class SetUserSubscriptionView(APIView):
    def post(self, request):
        # Получите id пользователя и данные о подписке из запроса
        user_id = request.data.get('user_id')
        subscription_plan = request.data.get('subscription_plan')

        # Проверка данных: если пользователь не подписан, то выбрасываем исключение
        if not user_id or not subscription_plan:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the user subscription (you'll need to implement the actual logic here)
        # For example, you might use a model to store the subscription details
        # subscription = Subscription.objects.create(user_id=user_id, plan=subscription_plan)

        return Response({'message': 'User subscription set successfully'}, status=status.HTTP_201_CREATED)


class DeleteUserSubscriptionView(APIView):
    def post(self, request):
        # Get the user ID from the request data
        user_id = request.data.get('user_id')

        # Validate the request data
        if not user_id:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the user subscription (you'll need to implement the actual logic here)
        # For example, you might use a model to store the subscription details
        # subscription = Subscription.objects.get(user_id=user_id)
        # subscription.delete()

        return Response({'message': 'User subscription deleted successfully'}, status=status.HTTP_200_OK)
