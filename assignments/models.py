from django.db import models
from lessons.models import Lesson
from accounts.models import Student


class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(blank=True, null=True)
    max_score = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.lesson.course.title})"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="submissions"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="submissions"
    )
    file_upload = models.FileField(upload_to="submissions/", blank=True, null=True)
    text_content = models.TextField(blank=True, help_text="Code or text submission")
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Grading
    score = models.PositiveIntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True)
    graded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("assignment", "student")

    def __str__(self):
        return f"{self.student.user.username} → {self.assignment.title}"

    @property
    def is_graded(self):
        return self.score is not None
