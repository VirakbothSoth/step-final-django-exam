from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("add/<slug:course_slug>/", views.add_review, name="add_review"),
    path("moderate/", views.moderate_reviews, name="moderate_reviews"),
    path("toggle/<int:pk>/", views.toggle_review_approval, name="toggle_review_approval"),
]
