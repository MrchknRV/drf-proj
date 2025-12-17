from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe
from django.conf import settings
from materials.models import Course, Lesson, Subscription
from materials.paginators import CustomPageNumberPagination
from materials.permissions import IsOwner, IsOwnerOrModerator, IsModerator
from materials.serializer import CourseSerializer, LessonSerializer, PaymentSerializer
from materials.services import create_stripe_product, create_stripe_price, create_strip_session
from users.models import Payments


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)


class SubscriptionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def subscribe(self, request, pk=None):
        course = Course.objects.get(pk=pk)
        _, created = Subscription.objects.get_or_create(user=request.user, course=course)

        if created:
            return Response({"post": "Вы успешно подписались на курс"}, status=status.HTTP_201_CREATED)
        return Response({"post": "Вы уже подписаны"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def unsubscribe(self, request, pk=None):
        course = Course.objects.get(pk=pk)
        deleted, _ = Subscription.objects.filter(user=request.user, course=course).delete()
        if deleted:
            return Response(status=status.HTTP_200_OK)
        return Response({"post": "Вы не были подписаны"}, status=status.HTTP_400_BAD_REQUEST)


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment_method = "cash" if serializer.validated_data.get("payment_method") == "Cash" else "card"
        paid_course = serializer.validated_data.get("paid_course")
        paid_amount = serializer.validated_data.get("paid_amount")

        if not paid_course or not paid_amount:
            raise serializers.ValidationError("Для оплаты необходимо выбрать курс и сумму")
        try:
            product = create_stripe_product(paid_course.name)
            price = create_stripe_price(product.id, paid_amount)
            session = create_strip_session(
                price_id=price.pk,
                payment_method=payment_method,
                success_url=Response({"post": "Success"}, status=status.HTTP_200_OK),
                cancel_url=Response({"post": "Canceled"}, status=status.HTTP_205_RESET_CONTENT),
                metadata={
                    "course_id": paid_course.pk,
                    "user_id": self.request.user.id,
                },
            )
            payment = serializer.save(
                user=self.request.user,
            )
            payment.stripe_session_id = session.pk
            payment.save()
            return Response({"session": session}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"post": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
