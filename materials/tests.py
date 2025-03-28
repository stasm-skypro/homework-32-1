from rest_framework import status
from rest_framework.test import APITestCase
from materials.models import Lesson, Course
from users.models import User

# Можно импортировать пользователя из users.models или получить таким способом
# User = get_user_model()


class LessonCreateAPIViewTestCase(APITestCase):
    """Тестирование CRUD операций с уроками."""

    def setUp(self):
        """Создаём тестовые данные."""

        # Создаём тестового владельца
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@email.com",
            password="password"
        )

        # self.non_owner = User.objects.create_user(
        #     username="non_owner",
        #     email="non_owner@email.com",
        #     password="password"
        # )
        #
        # self.moderator = User.objects.create_user(
        #     username="moderator",
        #     email="moderator@email.com",
        #     password="password",
        #     is_staff=True
        # )

        # Создаём тестовый курс
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Course Description",
            owner=self.owner
        )

        # Создаём тестовый урок
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test Description",
            course=self.course,
            owner=self.owner
        )

        # Создаём тестовые URL-ы
        self.lessons_create_url = "/lesson/create/"
        self.lessons_list_url = "/lesson/list/"
        self.lesson_url = f"/lesson/list/{self.lesson.id}/"
        self.lesson_update_url = f"/lesson/update/{self.lesson.id}/"
        self.lesson_delete_url = f"/lesson/delete/{self.lesson.id}/"


    def test_create_lesson_owner(self):
        """Владелец может создать урок."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.lessons_create_url,
            {
                "name": "New Lesson",
                "description": "New Description",
                "course": self.course.id,
            },
        )

        # Проверяем, что урок создан
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_list_lessons_authenticated(self):
        """Владелец может просматривать список уроков."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.lessons_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson_owner(self):
        """Владелец может просматривать свой урок."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_owner(self):
        """Владелец может обновлять свой урок."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(
            self.lesson_update_url,
            {
                "name": "Updated Lesson",
                "description": "Updated Description",
                "course": self.course.id,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_owner(self):
        """Владелец может удалять свой урок."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
