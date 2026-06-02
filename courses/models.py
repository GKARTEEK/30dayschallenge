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

    # COURSE PRICE
    price = models.IntegerField(
        default=99
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title


# =========================
# Enrollment Model
# =========================

class Enrollment(models.Model):

    # =========================
    # USER
    # =========================

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # =========================
    # COURSE
    # =========================

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    referral_code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # =========================
    # ENROLLED DATE
    # =========================

    enrolled_at = models.DateField(
        auto_now_add=True
    )

    # =========================
    # PAYMENT STATUS
    # =========================

    is_paid = models.BooleanField(
        default=False
    )

    # =========================
    # RAZORPAY PAYMENT ID
    # =========================

    payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # =========================
    # RAZORPAY ORDER ID
    # =========================

    order_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # =========================
    # ADMIN FREE ACCESS
    # =========================

    is_free_access = models.BooleanField(
        default=False
    )

    # =========================
    # PREVENT DUPLICATES
    # =========================

    class Meta:

        unique_together = ['user', 'course']

    # =========================
    # STRING REPRESENTATION
    # =========================

    def __str__(self):

        return (
            f"{self.user.username}"
            f" - "
            f"{self.course.title}"
        )        # =========================
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

    thumbnail = models.URLField(
    blank=True,
    null=True
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

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    correct_answer = models.CharField(
        max_length=200,
        choices=[
            ('option1', 'Option 1'),
            ('option2', 'Option 2'),
            ('option3', 'Option 3'),
            ('option4', 'Option 4'),
        ]
    )

    class Meta:
        ordering = ['id']  # ✅ Consistent question order

    def get_options(self):  # ✅ Helper for template
        return [
            ('option1', self.option1),
            ('option2', self.option2),
            ('option3', self.option3),
            ('option4', self.option4),
        ]

    def get_correct_answer_text(self):  # ✅ Helper to show correct answer
        mapping = {
            'option1': self.option1,
            'option2': self.option2,
            'option3': self.option3,
            'option4': self.option4,
        }
        return mapping.get(self.correct_answer, '')

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

    score = models.IntegerField(default=0)

    total_questions = models.IntegerField(default=0)

    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'lesson']  # ✅ No duplicate attempts

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

class Referral(models.Model):

    referrer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='referrals_made'
    )

    referred_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='referred_by'
    )

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE
    )

    commission = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )