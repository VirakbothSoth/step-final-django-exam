# LearnHub – Django Online Learning Platform Project

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

*We already have a requirements.txt*
```
pip install django
pip install pillow               # ImageField support
pip install django-crispy-forms
pip install crispy-bootstrap5
```

---

## Setup Guide

### 1. Download/Clone the Repository

### 2. Make a Virtual Enviroment
*for Windows*
```
py -m venv .env
```

### 3. Enter your Enviroment
*for Windows*
```
.env\Scripts\activate
```

### 4. Install the requirements
```
pip install -r requirements.txt
```

### 5. Run the Server
```
py manage.py runserver
```

---

## Sample Credentials

These are the main available users within my project

| Role | Username | Password |
|---|---|---|
| Student | `student1` | `pass1234` |
| Instructor | `instructor1` | `pass1234` |
| Employee | `employee1` | `pass1234` |

*Although, you may create your own using the register feature.*

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
- For production, replace SQLite with PostgreSQL and set `DEBUG = False`.
