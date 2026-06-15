from django import forms
from .models import Course, Category, Tag


class CourseForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Course
        fields = [
            "title", "slug", "description", "category", "tags",
            "price", "thumbnail", "level", "is_published",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "slug": forms.TextInput(attrs={"placeholder": "auto-filled or custom"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "icon"]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "slug"]
