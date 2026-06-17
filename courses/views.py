from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from .models import Course, Category, Tag
from .forms import CourseForm, CategoryForm, TagForm
from enrollments.models import Enrollment



def course_list(request):
    """Public course browse page with filters."""
    courses = Course.objects.filter(is_published=True).select_related(
        "instructor__user", "category"
    )

    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")
    instructor_id = request.GET.get("instructor")

    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    if tag_slug:
        courses = courses.filter(tags__slug=tag_slug)
    if instructor_id:
        courses = courses.filter(instructor__id=instructor_id)

    context = {
        "courses": courses,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "selected_category": category_slug,
        "selected_tag": tag_slug,
    }
    return render(request, "courses/course_list.html", context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    is_enrolled = False
    if request.user.is_authenticated and request.user.role == "student":
        is_enrolled = Enrollment.objects.filter(
            student=request.user.student_profile, course=course
        ).exists()

    context = {
        "course": course,
        "lessons": course.lessons.order_by("order"),
        "reviews": course.reviews.select_related("student__user").order_by("-created_at"),
        "is_enrolled": is_enrolled,
    }
    return render(request, "courses/course_detail.html", context)


@login_required
def course_create(request):
    if request.user.role not in ("instructor", "employee"):
        messages.error(request, "Permission denied.")
        return redirect("courses:course_list")

    form = CourseForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        course = form.save(commit=False)
        if request.user.role == "instructor":
            course.instructor = request.user.instructor_profile
        if not course.slug:
            course.slug = slugify(course.title)
        course.save()
        form.save_m2m()
        messages.success(request, "Course created successfully!")
        return redirect("courses:course_detail", slug=course.slug)

    return render(request, "courses/course_form.html", {"form": form, "action": "Create"})


@login_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.user.role == "instructor" and course.instructor != request.user.instructor_profile:
        messages.error(request, "You can only edit your own courses.")
        return redirect("courses:course_list")
    if request.user.role == "student":
        messages.error(request, "Permission denied.")
        return redirect("courses:course_list")

    form = CourseForm(request.POST or None, request.FILES or None, instance=course)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Course updated.")
        return redirect("courses:course_detail", slug=course.slug)

    return render(request, "courses/course_form.html", {"form": form, "action": "Edit", "course": course})


@login_required
def course_delete(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.user.role == "employee" or (
        request.user.role == "instructor" and course.instructor == request.user.instructor_profile
    ):
        if request.method == "POST":
            course.delete()
            messages.success(request, "Course deleted.")
            return redirect("courses:course_list")
        return render(request, "courses/course_confirm_delete.html", {"course": course})

    messages.error(request, "Permission denied.")
    return redirect("courses:course_list")


# ── Category & Tag management (employee only) ──────────────────────────────

@login_required
def category_list(request):
    if request.user.role != "employee":
        messages.error(request, "Permission denied.")
        return redirect("courses:course_list")
    categories = Category.objects.all()
    return render(request, "courses/category_list.html", {"categories": categories})


@login_required
def category_create(request):
    if request.user.role != "employee":
        messages.error(request, "Permission denied.")
        return redirect("courses:course_list")
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category created.")
        return redirect("courses:category_list")
    return render(request, "courses/category_form.html", {"form": form, "action": "Create"})


@login_required
def tag_list(request):
    if request.user.role != "employee":
        messages.error(request, "Permission denied.")
        return redirect("courses:course_list")
    tags = Tag.objects.all()
    return render(request, "courses/tag_list.html", {"tags": tags})


@login_required
def tag_create(request):
    if request.user.role != "employee":
        messages.error(request, "Permission denied.")
        return redirect("courses:course_list")
    form = TagForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tag created.")
        return redirect("courses:tag_list")
    return render(request, "courses/tag_form.html", {"form": form, "action": "Create"})

@login_required
def manage_tags(request):
    if request.user.role != 'employee':
        return redirect('dashboard')
    tags = Tag.objects.all().order_by('name')
    return render(request, 'courses/manage_tags.html', {'tags': tags})

@login_required
def tag_create(request):
    if request.user.role != 'employee':
        return redirect('dashboard')
    form = TagForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tag created successfully.')
        return redirect('courses:manage_tags')
    return render(request, 'courses/tag_form.html', {'form': form, 'action': 'Create'})

@login_required
def tag_edit(request, pk):
    if request.user.role != 'employee':
        return redirect('dashboard')
    tag = get_object_or_404(Tag, pk=pk)
    form = TagForm(request.POST or None, instance=tag)
    if form.is_valid():
        form.save()
        messages.success(request, 'Tag updated successfully.')
        return redirect('courses:manage_tags')
    return render(request, 'courses/tag_form.html', {'form': form, 'action': 'Edit', 'tag': tag})

@login_required
def tag_delete(request, pk):
    if request.user.role != 'employee':
        return redirect('dashboard')
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted.')
        return redirect('courses:manage_tags')
    return render(request, 'courses/tag_confirm_delete.html', {'tag': tag})