from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from users.models import Payments


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Lesson
        # fields = ["name", "description"]
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        # exclude = ("preview",)
        fields = ["name", "description", "lesson_count", "lessons", "owner", "is_subscribed"]
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    course = CourseSerializer(source="paid_course", read_only=True)
    lesson = LessonSerializer(source="paid_lesson", read_only=True)

    class Meta:
        model = Payments
        fields = ("id", "user", "course", "lesson", "payment_amount", "payment_method", "payment_date")
