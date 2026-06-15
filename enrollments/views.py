from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Enrollment, LessonProgress
from courses.models import Course
from lessons.models import Lesson


@login_required
def enroll(request, slug):
    if request.user.role != "student":
        messages.error(request, "Only students can enroll.")
        return redirect("courses:course_detail", slug=slug)

    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user.student_profile, course=course
    )
    if created:
        messages.success(request, f"Enrolled in {course.title}!")
    else:
        messages.info(request, "You are already enrolled.")
    return redirect("enrollments:my_courses")


@login_required
def my_courses(request):
    if request.user.role != "student":
        return redirect("accounts:login")

    enrollments = Enrollment.objects.filter(
        student=request.user.student_profile
    ).select_related("course", "course__instructor__user", "course__category")

    return render(request, "enrollments/my_courses.html", {"enrollments": enrollments})


@login_required
def course_learn(request, slug):
    """Course learning page with lesson list and progress."""
    if request.user.role != "student":
        messages.error(request, "Only students can access learning pages.")
        return redirect("courses:course_detail", slug=slug)

    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(
        Enrollment, student=request.user.student_profile, course=course
    )
    lessons = course.lessons.order_by("order")

    # Fetch or create progress records
    progress_map = {}
    for lesson in lessons:
        prog, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        progress_map[lesson.id] = prog

    context = {
        "course": course,
        "enrollment": enrollment,
        "lessons": lessons,
        "progress_map": progress_map,
    }
    return render(request, "enrollments/course_learn.html", context)


@login_required
def mark_lesson_complete(request, lesson_id):
    if request.user.role != "student":
        messages.error(request, "Permission denied.")
        return redirect("accounts:login")

    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = get_object_or_404(
        Enrollment, student=request.user.student_profile, course=lesson.course
    )
    prog, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    if not prog.completed:
        prog.completed = True
        prog.completed_at = timezone.now()
        prog.save()
        messages.success(request, f'"{lesson.title}" marked as complete!')

        # Auto-complete enrollment if all lessons done
        total = lesson.course.lessons.count()
        done = enrollment.lesson_progress.filter(completed=True).count()
        if done == total:
            enrollment.completed = True
            enrollment.completed_at = timezone.now()
            enrollment.save()
            messages.success(request, "🎉 Course completed!")

    return redirect("enrollments:course_learn", slug=lesson.course.slug)


@login_required
def all_enrollments(request):
    """Employee view of all enrollments."""
    if request.user.role != "employee":
        messages.error(request, "Permission denied.")
        return redirect("accounts:login")

    enrollments = Enrollment.objects.select_related(
        "student__user", "course"
    ).order_by("-enrolled_at")
    return render(request, "enrollments/all_enrollments.html", {"enrollments": enrollments})
