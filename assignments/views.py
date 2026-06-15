from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Assignment, Submission
from .forms import AssignmentForm, SubmissionForm, GradeSubmissionForm
from lessons.models import Lesson


@login_required
def assignment_create(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.user.role != "instructor" or lesson.course.instructor != request.user.instructor_profile:
        messages.error(request, "Permission denied.")
        return redirect("courses:course_detail", slug=lesson.course.slug)

    form = AssignmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        assignment = form.save(commit=False)
        assignment.lesson = lesson
        assignment.save()
        messages.success(request, "Assignment created.")
        return redirect("courses:course_detail", slug=lesson.course.slug)

    return render(request, "assignments/assignment_form.html", {"form": form, "lesson": lesson})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    user = request.user
    submission = None

    if user.role == "student":
        submission = Submission.objects.filter(
            assignment=assignment, student=user.student_profile
        ).first()

    context = {"assignment": assignment, "submission": submission}
    return render(request, "assignments/assignment_detail.html", context)


@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.user.role != "student":
        messages.error(request, "Only students can submit assignments.")
        return redirect("assignments:assignment_detail", pk=pk)

    existing = Submission.objects.filter(
        assignment=assignment, student=request.user.student_profile
    ).first()

    form = SubmissionForm(request.POST or None, request.FILES or None, instance=existing)
    if request.method == "POST" and form.is_valid():
        sub = form.save(commit=False)
        sub.assignment = assignment
        sub.student = request.user.student_profile
        sub.submitted_at = timezone.now()
        sub.save()
        messages.success(request, "Submission saved!")
        return redirect("assignments:assignment_detail", pk=pk)

    return render(request, "assignments/submission_form.html", {"form": form, "assignment": assignment})


@login_required
def grade_submission(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    if request.user.role != "instructor" or submission.assignment.lesson.course.instructor != request.user.instructor_profile:
        messages.error(request, "Permission denied.")
        return redirect("accounts:instructor_dashboard")

    form = GradeSubmissionForm(request.POST or None, instance=submission)
    if request.method == "POST" and form.is_valid():
        graded = form.save(commit=False)
        graded.graded_at = timezone.now()
        graded.save()
        messages.success(request, "Submission graded.")
        return redirect("assignments:submissions_list", pk=submission.assignment.pk)

    return render(request, "assignments/grade_form.html", {"form": form, "submission": submission})


@login_required
def submissions_list(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.user.role != "instructor" or assignment.lesson.course.instructor != request.user.instructor_profile:
        messages.error(request, "Permission denied.")
        return redirect("accounts:instructor_dashboard")

    submissions = assignment.submissions.select_related("student__user")
    return render(request, "assignments/submissions_list.html", {
        "assignment": assignment,
        "submissions": submissions,
    })
