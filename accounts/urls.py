from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/student/", views.register_student, name="register_student"),
    path("register/instructor/", views.register_instructor, name="register_instructor"),
    path("dashboard/student/", views.student_dashboard, name="student_dashboard"),
    path("dashboard/instructor/", views.instructor_dashboard, name="instructor_dashboard"),
    path("dashboard/employee/", views.employee_dashboard, name="employee_dashboard"),
    path("profile/", views.profile_view, name="profile"),
]
