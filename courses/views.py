from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.db.models import Count,Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from accounts.models import ReferralProfile
import razorpay
import hmac
import hashlib
from datetime import date

from .models import (
    Course,
    Enrollment,
    Lesson,
    QuizQuestion,
    QuizAttempt,
    UserProfile,
    CompletedLesson,
    CommunityPost,
    Badge,
    PostComment,
    PostLike
)


# =========================
# HOME / COURSES
# =========================

def course_list(request):

    courses = Course.objects.all()

    context = {
        'courses': courses
    }

    return render(
        request,
        'courses.html',
        context
    )


# =========================
# ENROLL COURSE
# ✅ Just redirect to payment — never create enrollment here
# =========================

@login_required(login_url='login')
def enroll_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    # ✅ If already paid, go straight to lessons
    already_paid = Enrollment.objects.filter(
        user=request.user,
        course=course,
        is_paid=True
    ).exists()

    if already_paid:
        return redirect(
            'course_lessons',
            course_id=course.id
        )

    # ✅ Not paid — redirect to payment page only
    return redirect(
        f'/payment/?course_id={course.id}'
    )


# =========================
# COURSE LESSONS
# =========================
@login_required(login_url='login')
def course_lessons(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    enrollments = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).order_by('-is_paid', '-is_free_access')

    enrollment = enrollments.first()

    print("========== COURSE LESSONS ==========")
    print("User:", request.user.username)

    if enrollment:
        print("Enrollment ID:", enrollment.id)
        print("Paid:", enrollment.is_paid)
        print("Free Access:", enrollment.is_free_access)
    else:
        print("No Enrollment Found")

    print("===================================")

    if not enrollment:
        return redirect('courses')

    duplicate_enrollments = enrollments.exclude(
        id=enrollment.id
    )

    if duplicate_enrollments.exists():
        duplicate_enrollments.delete()

    if (
        not enrollment.is_paid
        and
        not enrollment.is_free_access
    ):
        return redirect(
            f'/payment/?course_id={course.id}'
        )

    days_passed = (
        date.today() - enrollment.enrolled_at
    ).days + 1

    lessons = Lesson.objects.filter(
        course=course
    ).order_by('day')

    progress = int(
        (days_passed / course.total_days) * 100
    )

    if progress > 100:
        progress = 100

    context = {
        'course': course,
        'lessons': lessons,
        'days_passed': days_passed,
        'progress': progress
    }

    return render(
        request,
        'course_lessons.html',
        context
    )

# =========================
# LESSON DETAIL
# =========================

@login_required(login_url='login')
def lesson_detail(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=lesson.course
    )

    # =========================
    # PAYMENT CHECK
    # =========================

    if not enrollment.is_paid and not enrollment.is_free_access:
        return redirect(
            'payment_page',
            course_id=lesson.course.id
        )

    # =========================
    # DAILY UNLOCK
    # =========================

    days_passed = (
        date.today() - enrollment.enrolled_at
    ).days + 1

    if lesson.day > days_passed:
        return redirect(
            'course_lessons',
            course_id=lesson.course.id
        )

    # =========================
    # LESSONS
    # =========================

    lessons = Lesson.objects.filter(
        course=lesson.course
    ).order_by('day')

    # =========================
    # QUIZ QUESTIONS
    # =========================

    quiz_questions = QuizQuestion.objects.filter(
        lesson=lesson
    )

    # =========================
    # PROGRESS
    # =========================

    progress = int(
        (lesson.day / lesson.course.total_days) * 100
    )

    # =========================
    # COMPLETED CHECK
    # =========================

    completed = CompletedLesson.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()

    # =========================
    # QUIZ ATTEMPT
    # =========================

    existing_attempt = QuizAttempt.objects.filter(
        user=request.user,
        lesson=lesson
    ).first()

    score = None
    total_questions = quiz_questions.count()

    # =========================
    # QUIZ SUBMISSION
    # =========================

    if request.method == "POST":

        if existing_attempt:
            score = existing_attempt.score
            total_questions = existing_attempt.total_questions

        else:
            correct_answers = 0

            for quiz in quiz_questions:

                selected_answer = request.POST.get(
                    f"quiz_{quiz.id}"
                )

                if selected_answer == quiz.correct_answer:
                    correct_answers += 1

            score = correct_answers

            QuizAttempt.objects.create(
                user=request.user,
                lesson=lesson,
                score=score,
                total_questions=total_questions
            )

            if score > 0:

                profile = UserProfile.objects.get(
                    user=request.user
                )

                profile.xp += score * 10
                profile.coins += score * 2
                profile.level = max(
                    profile.level,
                    (profile.xp // 500) + 1
                )
                profile.save()

    context = {
        'lesson': lesson,
        'lessons': lessons,
        'quiz_questions': quiz_questions,
        'progress': progress,
        'days_passed': days_passed,
        'score': score,
        'total_questions': total_questions,
        'existing_attempt': existing_attempt,
        'completed': completed
    }

    return render(
        request,
        'lesson_detail.html',
        context
    )


# =========================
# COMPLETE LESSON
# =========================

@login_required(login_url='login')
def complete_lesson(request, lesson_id):

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id
    )

    already_completed = CompletedLesson.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()

    if not already_completed:

        CompletedLesson.objects.create(
            user=request.user,
            lesson=lesson
        )

        profile = UserProfile.objects.get(
            user=request.user
        )

        profile.xp += 100
        profile.coins += 25
        profile.completed_lessons += 1
        profile.level = (profile.xp // 500) + 1
        profile.save()

        # =========================
        # BADGES SYSTEM
        # =========================

        if profile.completed_lessons == 1:
            Badge.objects.get_or_create(
                user=request.user,
                title='First Step',
                defaults={
                    'icon': '🚀',
                    'description': 'Completed first lesson'
                }
            )

        if profile.completed_lessons == 5:
            Badge.objects.get_or_create(
                user=request.user,
                title='Fast Learner',
                defaults={
                    'icon': '⚡',
                    'description': 'Completed 5 lessons'
                }
            )

        if profile.completed_lessons == 10:
            Badge.objects.get_or_create(
                user=request.user,
                title='Consistency King',
                defaults={
                    'icon': '🔥',
                    'description': 'Completed 10 lessons'
                }
            )

        if profile.xp >= 1000:
            Badge.objects.get_or_create(
                user=request.user,
                title='1000 XP Club',
                defaults={
                    'icon': '💎',
                    'description': 'Reached 1000 XP'
                }
            )

    return redirect(
        'lesson_detail',
        lesson_id=lesson.id
    )


# =========================
# LEADERBOARD
# =========================

@login_required(login_url='login')
def leaderboard(request):

    profiles = UserProfile.objects.all().order_by(
        '-xp',
        '-level'
    )

    context = {
        'profiles': profiles
    }

    return render(
        request,
        'leaderboard.html',
        context
    )


# =========================
# COMMUNITY
# =========================

@login_required(login_url='login')
def community(request):

    if request.method == "POST":

        content = request.POST.get('content')

        if content:
            CommunityPost.objects.create(
                user=request.user,
                content=content
            )

    posts = CommunityPost.objects.all().order_by(
        '-created_at'
    )

    top_users = UserProfile.objects.all().order_by(
        '-xp'
    )[:5]

    liked_posts = PostLike.objects.filter(
        user=request.user
    ).values_list('post_id', flat=True)

    context = {
        'posts': posts,
        'top_users': top_users,
        'liked_posts': liked_posts
    }

    return render(
        request,
        'community.html',
        context
    )


# =========================
# LIKE / UNLIKE POST
# =========================

@login_required(login_url='login')
def like_post(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        id=post_id
    )

    already_liked = PostLike.objects.filter(
        post=post,
        user=request.user
    ).first()

    if already_liked:

        already_liked.delete()
        post.likes -= 1

        if post.likes < 0:
            post.likes = 0

        post.save()

    else:

        PostLike.objects.create(
            post=post,
            user=request.user
        )

        post.likes += 1
        post.save()

    return redirect('community')


# =========================
# COMMENT SYSTEM
# =========================

@login_required(login_url='login')
def add_comment(request, post_id):

    post = get_object_or_404(
        CommunityPost,
        id=post_id
    )

    if request.method == "POST":

        content = request.POST.get('content')

        if content:
            PostComment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

    return redirect('community')


# =========================
# CERTIFICATE
# =========================

@login_required(login_url='login')
def generate_certificate(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    total_lessons = Lesson.objects.filter(
        course=course
    ).count()

    completed_lessons = CompletedLesson.objects.filter(
        user=request.user,
        lesson__course=course
    ).count()

    if completed_lessons < total_lessons:
        return redirect(
            'course_lessons',
            course_id=course.id
        )

    context = {
        'course': course,
        'user': request.user
    }

    return render(
        request,
        'certificate.html',
        context
    )

# =========================
# PROFILE PAGE
# =========================

@login_required(login_url='login')
def profile_page(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    badges = Badge.objects.filter(
        user=request.user
    )

    posts = CommunityPost.objects.filter(
        user=request.user
    ).order_by('-created_at')

    certificates = Enrollment.objects.filter(
        user=request.user,
        is_paid=True
    )

    total_users = UserProfile.objects.count()

    rank = UserProfile.objects.filter(
        xp__gt=profile.xp
    ).count() + 1

    # =========================
    # REFERRAL DATA
    # =========================

    referral_profile, created = ReferralProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'referral_code': request.user.username.upper()
        }
    )

    referred_users = ReferralProfile.objects.filter(
        referred_by=referral_profile
    ).annotate(
        enrolled_courses=Count(
            'user__enrollment',
            filter=Q(
                user__enrollment__is_paid=True
            )
        )
    )

    total_enrollments = sum(
        user.enrolled_courses
        for user in referred_users
    )

    context = {
        'profile': profile,
        'badges': badges,
        'posts': posts,
        'certificates': certificates,
        'rank': rank,
        'total_users': total_users,

        # Referral
        'referral_profile': referral_profile,
        'referred_users': referred_users,
        'total_enrollments': total_enrollments,
    }

    return render(
        request,
        'profile.html',
        context
    )
# =========================
# PAYMENT PAGE
# ✅ Creates temporary enrollment with order_id only
# =========================
@login_required(login_url='login')
def payment_page(request):

    course_id = request.GET.get('course_id')

    course = get_object_or_404(
        Course,
        id=course_id
    )

    already_enrolled = Enrollment.objects.filter(
        user=request.user,
        course=course,
        is_paid=True
    ).exists()

    if already_enrolled:
        return redirect(
            'course_lessons',
            course_id=course.id
        )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    amount = 14900  # ₹1 test

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1",
        "notes": {
            "course_id": str(course.id),
            "user_id": str(request.user.id)
        }
    })

    context = {
        "course": course,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    }

    return render(
        request,
        'payment.html',
        context
    )


@csrf_exempt
def payment_success(request):


    if request.method != "POST":
        return redirect("courses")

    payment_id = request.POST.get("razorpay_payment_id")
    order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")


    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:

        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })

        payment_data = client.payment.fetch(
            payment_id
        )

        course_id = payment_data["notes"]["course_id"]
        user_id = payment_data["notes"]["user_id"]

        

        user = User.objects.get(
            id=user_id
        )

        course = Course.objects.get(
            id=course_id
        )

        enrollment, created = Enrollment.objects.get_or_create(
            user=user,
            course=course
        )

        enrollment.is_paid = True
        enrollment.payment_id = payment_id
        enrollment.order_id = order_id
        enrollment.save()

        return redirect(
            "course_lessons",
            course_id=course.id
        )

    except Exception as e:

        print("PAYMENT ERROR:", str(e))

        return redirect("courses")
        
        # =========================
# STATIC PAGES
# =========================

def about_page(request):
    return render(request, 'about.html')


def contact_page(request):
    return render(request, 'contact.html')


def privacy_page(request):
    return render(request, 'privacy.html')


def terms_page(request):
    return render(request, 'terms.html')