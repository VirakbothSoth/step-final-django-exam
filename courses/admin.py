from django.contrib import admin
from .models import Category, Tag, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "instructor", "category", "level", "price", "is_published", "created_at"]
    list_filter = ["is_published", "level", "category"]
    search_fields = ["title", "instructor__user__username"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
