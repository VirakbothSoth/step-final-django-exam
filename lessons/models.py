from django.db import models
from courses.models import Course


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    # Content
    video_file = models.FileField(upload_to="lesson_videos/", blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube/Vimeo embed URL")
    document = models.FileField(upload_to="lesson_docs/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} – #{self.order} {self.title}"
