from rest_framework import routers
from django.urls import path

from materials import views

app_name = "materials"

router = routers.DefaultRouter()
router.register(r"course", views.CourseViewSet, basename="course")

urlpatterns = [
                  path("lesson/", views.LessonListAPIView.as_view(), name="lesson-list"),
                  path("lesson/create/", views.LessonCreateAPIView.as_view(), name="lesson-create"),
                  path("lesson/update/<int:pk>/", views.LessonUpdateAPIView.as_view(), name="lesson-update"),
                  path("lesson/delete/<int:pk>/", views.LessonDeleteAPIView.as_view(), name="lesson-delete"),
                  path("lesson/<int:pk>/", views.LessonRetrieveAPIView.as_view(), name="lesson-retrieve"),
              ] + router.urls
