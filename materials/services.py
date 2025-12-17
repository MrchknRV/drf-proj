import stripe
from django.conf import settings


stripe_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course_name):
    try:
        product = stripe.Product.create(name=course_name)
        return product
    except stripe.StripeError as ex:
        return str(ex)


def create_stripe_price(product_id, amount):
    try:
        price = stripe.Price.create(
            amount=int(amount) * 100,
            currency="usd",
            source=product_id
        )
        return price
    except stripe.StripeError as ex:
        return str(ex)


def create_strip_session(price_id, payment_method, success_url, cancel_url, metadata):
    try:
        session = stripe.Session.create(
            payment_method_types = [payment_method],
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata
        )
        return session
    except stripe.StripeError as ex:
        return str(ex)