from django.db import models
from accounts.models import Student
from courses.models import Course


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)  # Employee can set False to moderate
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("course", "student")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student.user.username} – {self.course.title} ({self.rating}★)"
