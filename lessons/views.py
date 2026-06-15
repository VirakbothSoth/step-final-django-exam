from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lesson
from .forms import LessonForm
from courses.models import Course


@login_required
def lesson_create(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    # Only instructor who owns it, or employee
    if request.user.role == "instructor" and course.instructor != request.user.instructor_profile:
        messages.error(request, "Permission denied.")
        return redirect("courses:course_detail", slug=course_slug)
    if request.user.role == "student":
        messages.error(request, "Permission denied.")
        return redirect("courses:course_detail", slug=course_slug)

    form = LessonForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        lesson = form.save(commit=False)
        lesson.course = course
        lesson.save()
        messages.success(request, "Lesson added.")
        return redirect("courses:course_detail", slug=course_slug)

    return render(request, "lessons/lesson_form.html", {"form": form, "course": course, "action": "Add"})


@login_required
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course = lesson.course

    if request.user.role == "instructor" and course.instructor != request.user.instructor_profile:
        messages.error(request, "Permission denied.")
        return redirect("courses:course_detail", slug=course.slug)
    if request.user.role == "student":
        messages.error(request, "Permission denied.")
        return redirect("courses:course_detail", slug=course.slug)

    form = LessonForm(request.POST or None, request.FILES or None, instance=lesson)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Lesson updated.")
        return redirect("courses:course_detail", slug=course.slug)

    return render(request, "lessons/lesson_form.html", {"form": form, "course": course, "action": "Edit"})


@login_required
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    course = lesson.course

    if request.user.role == "instructor" and course.instructor != request.user.instructor_profile:
        messages.error(request, "Permission denied.")
        return redirect("courses:course_detail", slug=course.slug)
    if request.user.role == "student":
        messages.error(request, "Permission denied.")
        return redirect("courses:course_detail", slug=course.slug)

    if request.method == "POST":
        lesson.delete()
        messages.success(request, "Lesson deleted.")
        return redirect("courses:course_detail", slug=course.slug)

    return render(request, "lessons/lesson_confirm_delete.html", {"lesson": lesson})


@login_required
def lesson_detail(request, pk):
    """Lesson view for enrolled students."""
    lesson = get_object_or_404(Lesson, pk=pk)
    context = {"lesson": lesson, "course": lesson.course}
    return render(request, "lessons/lesson_detail.html", context)
