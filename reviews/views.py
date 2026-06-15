from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Review
from courses.models import Course
from enrollments.models import Enrollment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4}),
            "rating": forms.Select(),
        }


@login_required
def add_review(request, course_slug):
    if request.user.role != "student":
        messages.error(request, "Only students can leave reviews.")
        return redirect("courses:course_detail", slug=course_slug)

    course = get_object_or_404(Course, slug=course_slug)
    enrolled = Enrollment.objects.filter(
        student=request.user.student_profile, course=course
    ).exists()
    if not enrolled:
        messages.error(request, "You must be enrolled to review this course.")
        return redirect("courses:course_detail", slug=course_slug)

    existing = Review.objects.filter(course=course, student=request.user.student_profile).first()
    form = ReviewForm(request.POST or None, instance=existing)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.course = course
        review.student = request.user.student_profile
        review.save()
        messages.success(request, "Review submitted!")
        return redirect("courses:course_detail", slug=course_slug)

    return render(request, "reviews/review_form.html", {"form": form, "course": course})


@login_required
def moderate_reviews(request):
    if request.user.role != "employee":
        messages.error(request, "Permission denied.")
        return redirect("accounts:login")

    reviews = Review.objects.select_related("student__user", "course").order_by("-created_at")
    return render(request, "reviews/moderate_reviews.html", {"reviews": reviews})


@login_required
def toggle_review_approval(request, pk):
    if request.user.role != "employee":
        messages.error(request, "Permission denied.")
        return redirect("accounts:login")

    review = get_object_or_404(Review, pk=pk)
    review.is_approved = not review.is_approved
    review.save()
    status = "approved" if review.is_approved else "hidden"
    messages.success(request, f"Review {status}.")
    return redirect("reviews:moderate_reviews")
