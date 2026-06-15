from django.urls import path
from . import views

app_name = "enrollments"

urlpatterns = [
    path("enroll/<slug:slug>/", views.enroll, name="enroll"),
    path("my-courses/", views.my_courses, name="my_courses"),
    path("learn/<slug:slug>/", views.course_learn, name="course_learn"),
    path("complete/<int:lesson_id>/", views.mark_lesson_complete, name="mark_lesson_complete"),
    path("all/", views.all_enrollments, name="all_enrollments"),
]
