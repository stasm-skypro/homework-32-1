from django.db import models


class Course(models.Model):
    """Модель курса."""

    name = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    image = models.ImageField(upload_to="courses/", blank=True, null=True, verbose_name="Превью курса")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Владелец курса")
    video = models.TextField(verbose_name="Видео курса", blank=True, null=True)

    def __str__(self):
        """Метод для отображения объекта курса в админке."""
        return self.name

    class Meta:
        """Мета-класс для отображения имени модели в админке."""

        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока."""

    name = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    image = models.ImageField(upload_to="lessons/", blank=True, null=True, verbose_name="Превью урока")
    video = models.FileField(upload_to="lessons/", blank=True, null=True, verbose_name="Видео урока")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Владелец урока")

    def __str__(self):
        """Метод для отображения объекта урока в админке."""
        return f"{self.name} - {self.course.name}"

    class Meta:
        """Мета-класс для отображения имени модели в админке."""

        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
