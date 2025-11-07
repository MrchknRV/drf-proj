from rest_framework import serializers

from materials.models import Course, Lesson
from users.models import User, Payments


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
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payments
        fields = (
            "id",
            "user",
            "paid_course",
            "paid_lesson",
            "payment_amount",
            "payment_method",
            "payment_date"
        )
