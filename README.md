# LearnHub – Django Online Learning Platform

A full-featured online learning platform supporting three roles: **Student**, **Instructor**, and **Employee**.

---

## Features

| Feature | Roles |
|---|---|
| Custom user model with role field | All |
| Role-based dashboards after login | All |
| Browse & filter courses (category, tag, instructor) | All |
| Enroll in courses | Student |
| Lesson progress tracking | Student |
| Create & manage courses | Instructor, Employee |
| Add/edit lessons (video, PDF, description) | Instructor, Employee |
| Manage categories & tags | Employee |
| View all enrollments | Employee |
| Create assignments per lesson | Instructor |
| Submit assignments (file or text) | Student |
| Grade submissions with feedback | Instructor |
| Course reviews & ratings | Student |
| Moderate reviews | Employee |
| Django admin for all models | Superuser / Employee |

---

## Tech Stack

- **Python** 3.10+
- **Django** 4.2+
- **SQLite** (dev) — swap to PostgreSQL for production
- **Bootstrap 5** (CDN)
- **Font Awesome 6** (CDN)

---

## Required Packages

```
pip install django
pip install pillow               # ImageField support
pip install django-crispy-forms
pip install crispy-bootstrap5
```

Or create a `requirements.txt`:

```
django>=4.2
pillow>=10.0
django-crispy-forms>=2.0
crispy-bootstrap5>=0.7
```

---

## Setup Guide

### 1. Create the Django project

```bash
django-admin startproject learnhub .
```

> Make sure to run this **inside** the folder that contains all the app folders (`accounts`, `courses`, etc.), not above it.

### 2. Apply settings

Follow `SETTINGS_GUIDE.md` — paste the full example block into `learnhub/settings.py`.

**Critical:** `AUTH_USER_MODEL = "accounts.User"` must be set before any migration.

### 3. Run migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py makemigrations lessons
python manage.py makemigrations enrollments
python manage.py makemigrations assignments
python manage.py makemigrations reviews
python manage.py migrate
```

### 4. Create a superuser (Employee account)

```bash
python manage.py createsuperuser
```

Then open `/admin/` and:
- Set the superuser's `role` to `employee`
- Create an `Employee` profile linked to that user

### 5. Seed sample data (optional)

```bash
python manage.py shell
```

```python
from accounts.models import User, Student, Instructor, Employee
from courses.models import Category, Tag

# Create instructor
u = User.objects.create_user("instructor1", "inst@demo.com", "pass1234", role="instructor")
from accounts.models import Instructor
Instructor.objects.create(user=u, expertise="Web Development")

# Create student
s = User.objects.create_user("student1", "stu@demo.com", "pass1234", role="student")
from accounts.models import Student
Student.objects.create(user=s)

# Create category
Category.objects.create(name="Web Development", slug="web-development")
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## Sample Credentials

> Create these via the shell or admin after setup.

| Role | Username | Password |
|---|---|---|
| Student | `student1` | `pass1234` |
| Instructor | `instructor1` | `pass1234` |
| Employee | `employee1` | `pass1234` |

---

## Project Structure

```
learnhub/                  ← Django project config
accounts/                  ← User, Student, Instructor, Employee models + auth
courses/                   ← Course, Category, Tag models
lessons/                   ← Lesson model (video, PDF, description)
enrollments/               ← Enrollment, LessonProgress models
assignments/               ← Assignment, Submission models (bonus)
reviews/                   ← Review model (bonus)
templates/                 ← All HTML templates
static/css/                ← main.css
media/                     ← Uploaded files (gitignored)
screenshots/               ← Screenshots for submission
SETTINGS_GUIDE.md          ← Settings instructions
README.md                  ← This file
```

---

## Notes

- The `enrollments/templatetags/enrollment_tags.py` provides a `get_item` filter used in `course_learn.html` for dict lookups — make sure `{% load enrollment_tags %}` is present if you extend that template.
- All file uploads go to `media/` — add it to `.gitignore`.
- For production, replace SQLite with PostgreSQL and set `DEBUG = False`.
