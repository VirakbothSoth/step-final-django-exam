from django.db import models
from accounts.models import Student
from courses.models import Course
from lessons.models import Lesson


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("student", "course")
        ordering = ["-enrolled_at"]

    def __str__(self):
        return f"{self.student.user.username} → {self.course.title}"

    @property
    def progress_percent(self):
        total = self.course.lessons.count()
        if total == 0:
            return 0
        done = self.lesson_progress.filter(completed=True).count()
        return int((done / total) * 100)


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="lesson_progress"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="progress_records"
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("enrollment", "lesson")

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.enrollment.student.user.username} – {self.lesson.title}"
