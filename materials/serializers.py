from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Subscription
from .models import Course, Lesson
from .validators import DescriptionValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Урок."""

    class Meta:
        """Мета класс для сериализатора."""

        model = Lesson
        fields = "__all__"
        validators = [DescriptionValidator(field="description")]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Курс."""

    lessons_count = serializers.SerializerMethodField()  # Количество уроков
    is_subscribed = serializers.SerializerMethodField()  # Подписка

    @staticmethod
    def get_lessons_count(obj):
        """Получение количества уроков в курсе."""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Определяет, подписан ли текущий пользователь на курс."""
        user = self.context.get("request").user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    class Meta:
        """Мета класс для сериализатора."""

        model = Course
        fields = ["id", "name", "description", "lessons_count", "is_subscribed"]
        validators = [DescriptionValidator(field="description")]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детализации модели Курс."""

    lessons_count = serializers.SerializerMethodField()  # Количество уроков
    lessons = LessonSerializer(many=True, read_only=True)  # Уроки
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_lessons_count(obj):
        """Получение количества уроков в курсе."""
        return obj.lessons.count()

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseSerializer(course, context={"request": request})
        return Response(serializer.data)

    class Meta:
        """Мета класс для сериализатора."""

        model = Course
        fields = ["name", "description", "lessons_count", "lessons"]
