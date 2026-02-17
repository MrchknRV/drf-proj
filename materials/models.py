from django.db import models

from materials.validators import url_validator
# from django.contrib.auth import get_user_model
from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(upload_to="course/preview", blank=True, null=True, verbose_name="Превью")
    description = models.TextField(blank=True, null=True, verbose_name="Описание", validators=[url_validator])
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses", verbose_name="Владелец", blank=True, null=True
    )
    last_update = models.DateTimeField(null=True, blank=True, verbose_name="Последнее обновление")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "course"
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание", validators=[url_validator])
    preview = models.ImageField(upload_to="lesson/preview", blank=True, null=True, verbose_name="Превью")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео", validators=[url_validator])
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lessons", verbose_name="Владелец", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "lesson"
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.course.name}"

    class Meta:
        db_table = "subscription"
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
