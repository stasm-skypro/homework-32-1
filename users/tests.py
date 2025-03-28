from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Course
from users.models import Subscription

User = get_user_model()


class SubscriptionAPIViewTestCase(APITestCase):
    """Тесты для подписки на курс."""

    def setUp(self):
        """Создаёт тестовые данные."""

        # Создаём пользователей
        self.user = User.objects.create_user(username="user1", email="user1@email", password="password123")
        self.other_user = User.objects.create_user(username="user2", email="user2@email", password="password123")

        # Создаём тестовый курс
        self.course = Course.objects.create(name="Test Course", description="Test Description", owner=self.user)

        # URL для подписки
        # self.subscription_url = reverse("course", kwargs={"pk": self.course.id})
        self.subscription_url = f"/course/{self.course.id}/"

    def test_subscribe_to_course(self):
        """Тест подписки пользователя на курс."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.subscription_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    # def test_unsubscribe_from_course(self):
    #     """Тест отписки пользователя от курса."""
    #     Subscription.objects.create(user=self.user, course=self.course)
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post(self.subscription_url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
    #
    # def test_subscribe_unauthenticated(self):
    #     """Проверяет, что неавторизованный пользователь не может подписаться."""
    #     response = self.client.post(self.subscription_url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_subscribe_to_own_course(self):
    #     """Тест подписки на собственный курс (допустимо или нет)."""
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post(self.subscription_url)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_subscribe_already_subscribed(self):
    #     """Проверяет повторную подписку (должно быть обработано корректно)."""
    #     Subscription.objects.create(user=self.user, course=self.course)
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post(self.subscription_url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Отписка, если подписан
    #
    # def test_subscribe_other_user(self):
    #     """Тест подписки другого пользователя."""
    #     self.client.force_authenticate(user=self.other_user)
    #     response = self.client.post(self.subscription_url)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertTrue(Subscription.objects.filter(user=self.other_user, course=self.course).exists())
