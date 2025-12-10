# materials/tests.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription

User = get_user_model()


class MaterialsCRUDAndSubscriptionTest(APITestCase):

    def setUp(self):
        self.moderator_group, _ = Group.objects.get_or_create(name="Moderator")

        self.owner = User.objects.create_user(email="owner@test.com", password="123", username="owner")
        self.moderator = User.objects.create_user(email="mod@test.com", password="123", username="moderator")
        self.moderator.groups.add(self.moderator_group)
        self.student = User.objects.create_user(email="student@test.com", password="123", username="student")

        self.course = Course.objects.create(
            name="Django для профи",
            description="Крутой курс",
            owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            name="Урок 1",
            description="Введение в Django REST",
            course=self.course,
            owner=self.owner,
            video_url="https://www.youtube.com/watch?v=12345"
        )

    def test_create_lesson_as_owner_success(self):
        self.client.force_authenticate(self.owner)
        url = reverse("materials:lesson-create")
        data = {
            "name": "Новый урок от владельца",
            "description": "Тест",
            "course": self.course.id,
            "video_url": "https://www.youtube.com/watch?v=abc123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_as_moderator_forbidden(self):
        self.client.force_authenticate(self.moderator)
        url = reverse("materials:lesson-create")
        data = {"name": "Урок от модератора", "course": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_as_student_forbidden(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:lesson-create")
        data = {"name": "Попытка", "course": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson_as_owner_success(self):
        self.client.force_authenticate(self.owner)
        url = reverse("materials:lesson-update", args=[self.lesson.pk])
        response = self.client.patch(url, {"name": "Обновлённый урок"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновлённый урок")

    def test_update_lesson_as_student_forbidden(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:lesson-update", args=[self.lesson.pk])
        response = self.client.patch(url, {"name": "Хак"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_as_owner_success(self):
        self.client.force_authenticate(self.owner)
        url = reverse("materials:lesson-delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    def test_delete_lesson_as_student_forbidden(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:lesson-delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscribe_to_course_success(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:subscription-subscribe", args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.student, course=self.course).exists())

    def test_subscribe_twice_returns_400(self):
        Subscription.objects.create(user=self.student, course=self.course)
        self.client.force_authenticate(self.student)
        url = reverse("materials:subscription-subscribe", args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsubscribe_from_course_success(self):
        Subscription.objects.create(user=self.student, course=self.course)
        self.client.force_authenticate(self.student)
        url = reverse("materials:subscription-unsubscribe", args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # твой код возвращает 200
        self.assertFalse(Subscription.objects.filter(user=self.student, course=self.course).exists())

    def test_is_subscribed_field_true_for_subscribed(self):
        Subscription.objects.create(user=self.student, course=self.course)
        self.client.force_authenticate(self.student)
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])

    def test_is_subscribed_field_false_for_not_subscribed(self):
        self.client.force_authenticate(self.student)
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])

    def test_lesson_list_pagination_works(self):
        self.client.force_authenticate(self.owner)
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)