from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription

User = get_user_model()


class MaterialsTest(APITestCase):

    def setUp(self):
        self.moderator_group, _ = Group.objects.get_or_create(name="Moderator")

        self.owner = User.objects.create_user(email="owner@test.com", password="123", username="owner")
        self.student = User.objects.create_user(email="student@test.com", password="123", username="student")

        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание",
            owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            description="Описание урока",
            course=self.course,
            owner=self.owner,
            video_url="https://www.youtube.com/watch?v=12345"
        )

    def test_create_lesson_as_owner(self):
        self.client.force_authenticate(self.owner)
        url = reverse("materials:lesson-create")
        data = {
            "name": "Новый урок",
            "description": "Тест",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=abc123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_as_student_forbidden(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:lesson-create")
        data = {"name": "Попытка", "course": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson_as_owner(self):
        self.client.force_authenticate(self.owner)
        url = reverse("materials:lesson-update", args=[self.lesson.pk])
        response = self.client.patch(url, {"name": "Обновлено"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_as_student_forbidden(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:lesson-update", args=[self.lesson.pk])
        response = self.client.patch(url, {"name": "Хак"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_as_owner(self):
        self.client.force_authenticate(self.owner)
        url = reverse("materials:lesson-delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_as_student_forbidden(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:lesson-delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscribe_and_unsubscribe(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:subscription-subscribe", args=[self.course.pk])
        self.client.post(url)
        self.assertTrue(Subscription.objects.filter(user=self.student, course=self.course).exists())

        url = reverse("materials:subscription-unsubscribe", args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.student, course=self.course).exists())

    def test_is_subscribed_field(self):
        self.client.force_authenticate(self.owner)
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])

        Subscription.objects.create(user=self.owner, course=self.course)
        response = self.client.get(url)
        self.assertTrue(response.data["is_subscribed"])