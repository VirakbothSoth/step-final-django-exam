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
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Learn Django in 30 Days",
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "auto-filled or custom",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "What will students learn?",
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "min": "0",
                "step": "0.01",
            }),
            "category": forms.Select(attrs={
                "class": "form-select",
            }),
            "level": forms.Select(attrs={
                "class": "form-select",
            }),
            "thumbnail": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "icon"]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "slug"]
