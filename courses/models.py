from django.db import models
from django.contrib.auth.models import User
# =========================
# Course Model
# =========================

class Course(models.Model):

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    thumbnail = models.ImageField(
    upload_to='courses/',
    blank=True,
    null=True
    )

    total_days = models.IntegerField(
        default=30
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title

# =========================
# Enrollment Model
# =========================

# =========================
# Enrollment Model
# =========================

class Enrollment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    enrolled_at = models.DateField(
        auto_now_add=True
    )

    # PAYMENT STATUS

    is_paid = models.BooleanField(
        default=False
    )

    # RAZORPAY PAYMENT ID

    payment_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    # ADMIN FREE ACCESS

    is_free_access = models.BooleanField(
        default=False
    )

    def __str__(self):

        return f"{self.user.username} - {self.course.title}"
# =========================
# Lesson Model
# =========================

class Lesson(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    day = models.IntegerField()

    video_url = models.URLField(
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    # =========================
    # Assignment
    # =========================

    assignment_title = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    assignment_description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.course.title} - Day {self.day}"


# =========================
# MCQ Quiz Model
# =========================

class QuizQuestion(models.Model):

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='quiz_questions'
    )

    question = models.TextField()

    option1 = models.CharField(
        max_length=200
    )

    option2 = models.CharField(
        max_length=200
    )

    option3 = models.CharField(
        max_length=200
    )

    option4 = models.CharField(
        max_length=200
    )

    correct_answer = models.CharField(
        max_length=200
    )

    def __str__(self):

        return self.question


# =========================
# Quiz Attempt Model
# =========================

class QuizAttempt(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    score = models.IntegerField(
        default=0
    )

    total_questions = models.IntegerField(
        default=0
    )

    attempted_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.lesson.title}"


# =========================
# User Profile Model
# =========================

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    xp = models.IntegerField(
        default=0
    )

    coins = models.IntegerField(
        default=0
    )

    streak = models.IntegerField(
        default=0
    )

    level = models.IntegerField(
        default=1
    )

    completed_lessons = models.IntegerField(
        default=0
    )

    def __str__(self):

        return self.user.username

# =========================
# Completed Lesson Model
# =========================

class CompletedLesson(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE
    )

    completed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} completed {self.lesson.title}"

# =========================
# COMMUNITY POST
# =========================

class CommunityPost(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    likes = models.IntegerField(
        default=0
    )

    def __str__(self):

        return self.user.username

        # =========================
# BADGE MODEL
# =========================

class Badge(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    icon = models.CharField(
        max_length=20,
        default='🏆'
    )

    description = models.TextField()

    earned_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.title}"

        
# =========================
# POST COMMENT MODEL
# =========================

class PostComment(models.Model):

    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username

        # =========================
# POST LIKE MODEL
# =========================

class PostLike(models.Model):

    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name='post_likes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = ['post', 'user']

    def __str__(self):

        return f"{self.user.username} liked"