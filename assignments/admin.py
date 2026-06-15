from django.contrib import admin
from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["title", "lesson", "due_date", "max_score"]
    list_filter = ["lesson__course"]
    search_fields = ["title", "lesson__course__title"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["student", "assignment", "submitted_at", "score", "is_graded"]
    list_filter = ["assignment__lesson__course"]
    search_fields = ["student__user__username"]
