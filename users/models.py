from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="users/avatar", blank=True, null=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    country = models.CharField(max_length=56, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Payments(models.Model):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"

    PAYMENT_TYPE_CHOICES = [
        (CASH, "Наличные"),
        (CREDIT_CARD, "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        "materials.Course", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Оплаченный курс"
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Оплаченный курс"
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=12, choices=PAYMENT_TYPE_CHOICES, default=CASH)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"ОПЛАТА от {self.user.email}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
