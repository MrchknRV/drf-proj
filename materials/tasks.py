from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from .models import Subscription


@shared_task
def send_course_update(course_id, course_name):
    subscription = Subscription.objects.filter(course_id=course_id).select_related("user")
    emails = [subs.user.email for subs in subscription if subs.user.email]

    if not emails:
        return "Никто не подписан"

    try:
        send_mail(
            subject=f"Обновление курса: {course_name}",
            message=f"Курс - {course_name} был обновлен!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=False,
        )
        return f"Отправлено {len(emails)} сообщений"
    except Exception as ex:
        return str(ex)


User = get_user_model()


@shared_task
def block_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__gt=one_month_ago, is_active=True)
    count_inactive_users = inactive_users.update(is_active=False)
    print(f"Заблокировано неактивных пользователей: {count_inactive_users}")
    return count_inactive_users
