from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from materials.models import Course, Lesson


class UserManager(BaseUserManager):
    """
    Класс менеджера пользователей. Нужен для правильного создания пользователей и суперпользователей в кастомной
    модели пользователя.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Метод для создания обычного пользователя."""
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Метод для создания суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Проверка, чтобы избежать ситуаций, когда суперпользователь создаётся без нужных прав
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Класс пользователя. Модель 'Пользователь'."""

    username = models.CharField(
        max_length=150,
        verbose_name="Имя пользователя",
        help_text="Укажите ваше имя пользователя",
        unique=True,
        error_messages={"unique": "Пользователь с таким именем уже существует."},
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Укажите ваш email",
        error_messages={"unique": "Пользователь с таким email уже существует."},
    )

    phone = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        help_text="Укажите ваш номер телефона",
        blank=True,
        null=True,
    )

    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Укажите ваш город",
        blank=True,
        null=True,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        verbose_name="Аватар",
        help_text="Загрузите ваш аватар",
        blank=True,
        null=True,
    )

    is_moderator = models.BooleanField(
        default=False,
        verbose_name="Модератор",
        help_text="Пользователь является модератором",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        """Мета-класс модели пользователя."""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Метод для отображения объекта пользователя в админке."""
        return self.email

    def get_user_name(self):
        """Метод для получения имени пользователя."""
        return self.username


class Payment(models.Model):
    """Класс оплаты. Модель 'Оплата'."""

    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments"
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты"
    )

    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс"
    )

    lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма платежа",
        help_text="Укажите сумму оплаты",
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHODS,
        verbose_name="Способ оплаты",
    )

    class Meta:
        """Мета-класс модели оплаты."""

        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        """Метод для отображения объекта оплаты в админке."""
        return f"{self.user.email} - {self.amount} руб."


class Subscription(models.Model):
    """Класс подписки. Модель 'Подписка'."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )

    class Meta:
        """Мета-класс модели подписки."""

        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        """Метод для отображения объекта подписки в админке."""
        return f"{self.user.email} - {self.course.name}"
