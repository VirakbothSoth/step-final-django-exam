from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("instructor", "Instructor"),
        ("employee", "Employee"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def profile(self):
        if self.role == "student":
            return self.student_profile
        elif self.role == "instructor":
            return self.instructor_profile
        elif self.role == "employee":
            return self.employee_profile
        return None


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    date_of_birth = models.DateField(blank=True, null=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Student: {self.user.username}"


class Instructor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="instructor_profile"
    )
    expertise = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Instructor: {self.user.username}"


class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ("admin", "Administration"),
        ("support", "Support"),
        ("content", "Content"),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="employee_profile"
    )
    department = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES, default="admin"
    )
    employee_id = models.CharField(max_length=20, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Employee: {self.user.username} ({self.department})"
