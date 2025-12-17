from django.urls import path
from rest_framework import routers

from materials import views

app_name = "materials"

router = routers.DefaultRouter()
router.register(r"course", views.CourseViewSet, basename="course")
router.register(r"subscription", views.SubscriptionViewSet, basename="subscription")
router.register(r"payments", views.PaymentViewSet, basename="payments")

urlpatterns = [
    path("lesson/", views.LessonListAPIView.as_view(), name="lesson-list"),
    path("lesson/create/", views.LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lesson/update/<int:pk>/", views.LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lesson/delete/<int:pk>/", views.LessonDeleteAPIView.as_view(), name="lesson-delete"),
    path("lesson/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson-retrieve"),
    path("payments/", views.PaymentsListAPIView.as_view(), name="payments-list"),
    path("payment/success/", views.PaymentSuccessView.as_view()),
    path("payment/cancel/", views.PaymentCancelView.as_view()),
] + router.urls
