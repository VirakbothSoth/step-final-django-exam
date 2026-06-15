from django.urls import path
from . import views

app_name = "assignments"

urlpatterns = [
    path("create/<int:lesson_id>/", views.assignment_create, name="assignment_create"),
    path("<int:pk>/", views.assignment_detail, name="assignment_detail"),
    path("<int:pk>/submit/", views.submit_assignment, name="submit_assignment"),
    path("<int:pk>/grade/", views.grade_submission, name="grade_submission"),
    path("<int:pk>/submissions/", views.submissions_list, name="submissions_list"),
]
