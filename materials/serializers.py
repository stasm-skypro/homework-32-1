from rest_framework import serializers
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

    @staticmethod
    def get_lessons_count(obj):
        """Получение количества уроков в курсе."""
        return obj.lessons.count()

    class Meta:
        """Мета класс для сериализатора."""

        model = Course
        fields = ["id", "name", "description", "lessons_count"]
        validators = [DescriptionValidator(field="description")]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детализации модели Курс."""

    lessons_count = serializers.SerializerMethodField()  # Количество уроков
    lessons = LessonSerializer(many=True, read_only=True)  # Уроки

    @staticmethod
    def get_lessons_count(obj):
        """Получение количества уроков в курсе."""
        return obj.lessons.count()

    class Meta:
        """Мета класс для сериализатора."""

        model = Course
        fields = ["name", "description", "lessons_count", "lessons"]
