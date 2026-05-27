from django.contrib import admin
from .models import Enrollment
    
from .models import (
    Course,
    Enrollment,
    Lesson,
    QuizQuestion
)


# =========================
# Course Admin
# =========================

admin.site.register(Course)


# =========================
# Enrollment Admin
# =========================

admin.site.register(Enrollment)


# =========================
# Lesson Admin
# =========================

admin.site.register(Lesson)


# =========================
# Quiz Admin
# =========================

admin.site.register(QuizQuestion)
from .models import CommunityPost

admin.site.register(
    CommunityPost
)