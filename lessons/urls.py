from django.urls import path
from . import views

app_name = "lessons"

urlpatterns = [
    path("<int:pk>/", views.lesson_detail, name="lesson_detail"),
    path("add/<slug:course_slug>/", views.lesson_create, name="lesson_create"),
    path("<int:pk>/edit/", views.lesson_edit, name="lesson_edit"),
    path("<int:pk>/delete/", views.lesson_delete, name="lesson_delete"),
]
