from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Instructor, Employee


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role & Profile", {"fields": ("role", "avatar", "bio")}),
    )
    list_display = ["username", "email", "role", "is_active", "date_joined"]
    list_filter = ["role", "is_active"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "enrolled_at"]
    search_fields = ["user__username", "user__email"]


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ["user", "expertise", "joined_at"]
    search_fields = ["user__username", "expertise"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["user", "department", "employee_id", "joined_at"]
    search_fields = ["user__username", "employee_id"]
    list_filter = ["department"]
