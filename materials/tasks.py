from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

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
