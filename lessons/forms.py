from django import forms
from .models import Lesson


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description", "order", "video_file", "video_url", "document"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "video_url": forms.URLInput(attrs={"placeholder": "https://youtube.com/embed/..."}),
        }
