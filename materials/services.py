from datetime import timedelta

import stripe
from django.conf import settings
from django.utils import timezone

from .tasks import send_course_update

stripe_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course_name):
    try:
        product = stripe.Product.create(name=course_name)
        return product
    except stripe.StripeError as ex:
        return str(ex)


def create_stripe_price(product_id, amount):
    try:
        price = stripe.Price.create(amount=int(amount) * 100, currency="usd", source=product_id)
        return price
    except stripe.StripeError as ex:
        return str(ex)


def create_strip_session(price_id, success_url, cancel_url, metadata):
    try:
        session = stripe.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,
        )
        return session
    except stripe.StripeError as ex:
        return str(ex)


def notification_subscribers(course):
    if not course:
        return

    four_hours_ago = timezone.now() - timedelta(hours=4)
    if course.last_update is None or course.last_update < four_hours_ago:
        send_course_update.delay(course.id, course.name)
        course.last_update = timezone.now()
        course.save(update_fields=["last_update"])
