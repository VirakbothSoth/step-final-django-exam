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
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
        self.fields["password2"].widget = forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"
        if commit:
            user.save()
            Student.objects.create(user=user)
        return user


class InstructorRegisterForm(UserCreationForm):
    expertise = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Python, Django"})
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={"class": "form-control", "placeholder": "https://yoursite.com"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
        self.fields["password2"].widget = forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})

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
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Tell us about yourself..."}),
        }