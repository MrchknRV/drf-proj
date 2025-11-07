from rest_framework import serializers

from materials.models import Course, Lesson
from users.models import Payments, User


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        # fields = ["name", "description"]
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        # exclude = ("preview",)
        fields = ["name", "description", "lesson_count", "lessons"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    course = CourseSerializer(source="paid_course", read_only=True)
    lesson = LessonSerializer(source="paid_lesson", read_only=True)

    class Meta:
        model = Payments
        fields = ("id", "user", "course", "lesson", "payment_amount", "payment_method", "payment_date")
