from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("create/", views.course_create, name="course_create"),
    path("<slug:slug>/", views.course_detail, name="course_detail"),
    path("<slug:slug>/edit/", views.course_edit, name="course_edit"),
    path("<slug:slug>/delete/", views.course_delete, name="course_delete"),
    # Category
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    # Tags
    path("tags/", views.tag_list, name="tag_list"),
    path("tags/create/", views.tag_create, name="tag_create"),
]
