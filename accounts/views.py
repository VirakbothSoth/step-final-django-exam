from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, StudentRegisterForm, InstructorRegisterForm, ProfileUpdateForm
from courses.models import Course
from enrollments.models import Enrollment


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.first_name or user.username}!")
        return redirect_by_role(user)

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")


def register_student(request):
    form = StudentRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Student account created!")
        return redirect("accounts:student_dashboard")
    return render(request, "accounts/register_student.html", {"form": form})


def register_instructor(request):
    form = InstructorRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Instructor account created!")
        return redirect("accounts:instructor_dashboard")
    return render(request, "accounts/register_instructor.html", {"form": form})


def redirect_by_role(user):
    role_map = {
        "student": "accounts:student_dashboard",
        "instructor": "accounts:instructor_dashboard",
        "employee": "accounts:employee_dashboard",
    }
    from django.urls import reverse
    return redirect(role_map.get(user.role, "accounts:login"))


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect_by_role(request.user)

    enrollments = Enrollment.objects.filter(
        student=request.user.student_profile
    ).select_related("course", "course__instructor__user", "course__category")

    context = {
        "enrollments": enrollments,
        "total_courses": enrollments.count(),
        "completed": enrollments.filter(completed=True).count(),
    }
    return render(request, "accounts/student_dashboard.html", context)


@login_required
def instructor_dashboard(request):
    if request.user.role != "instructor":
        return redirect_by_role(request.user)

    courses = Course.objects.filter(
        instructor=request.user.instructor_profile
    ).prefetch_related("enrollments")

    context = {
        "courses": courses,
        "total_students": sum(c.enrollments.count() for c in courses),
        "published_courses": courses.filter(is_published=True).count(),
    }
    return render(request, "accounts/instructor_dashboard.html", context)


@login_required
def employee_dashboard(request):
    if request.user.role != "employee":
        return redirect_by_role(request.user)

    from accounts.models import User, Student, Instructor
    context = {
        "total_users": User.objects.count(),
        "total_students": Student.objects.count(),
        "total_instructors": Instructor.objects.count(),
        "total_courses": Course.objects.count(),
        "total_enrollments": Enrollment.objects.count(),
        "recent_courses": Course.objects.order_by("-created_at")[:5],
        "recent_enrollments": Enrollment.objects.order_by("-enrolled_at")[:5],
    }
    return render(request, "accounts/employee_dashboard.html", context)


@login_required
def profile_view(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})
