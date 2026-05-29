from django.contrib import admin

from .models import (
    Course,
    Enrollment,
    Lesson,
    QuizQuestion,
    QuizAttempt,        # ✅ Added
    CommunityPost
)


# =========================
# Course Admin
# =========================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['title', 'created_at']
    search_fields = ['title']


# =========================
# Enrollment Admin
# =========================

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = ['user', 'course', 'enrolled_at']
    list_filter   = ['course']
    search_fields = ['user__username']


# =========================
# Lesson Admin
# =========================

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display  = ['title', 'course', 'day']
    list_filter   = ['course']
    search_fields = ['title']


# =========================
# Quiz Question Admin
# =========================

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display  = ['question', 'lesson', 'correct_answer']
    list_filter   = ['lesson']
    search_fields = ['question']


# =========================
# Quiz Attempt Admin
# =========================

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display  = ['user', 'lesson', 'score', 'total_questions', 'attempted_at']
    list_filter   = ['lesson']
    search_fields = ['user__username']


# =========================
# Community Post Admin
# =========================

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display  = ['user', 'created_at']
    search_fields = ['user__username']

