from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Student, Instructor


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )


class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        if commit:
            user.save()
            Student.objects.create(user=user)
        return user


class InstructorRegisterForm(UserCreationForm):
    expertise = forms.CharField(max_length=200, required=False)
    website = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "instructor"
        if commit:
            user.save()
            Instructor.objects.create(
                user=user,
                expertise=self.cleaned_data.get("expertise", ""),
                website=self.cleaned_data.get("website", ""),
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "avatar", "bio"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }
