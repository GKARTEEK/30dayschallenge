from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)


from django.shortcuts import render

from .models import Course


from django.contrib.auth.decorators import login_required
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

from datetime import date


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
# =========================

@login_required(login_url='login')

# =========================
# ENROLL COURSE
# =========================

@login_required(login_url='login')
@login_required
def enroll_course(request, course_id):

    course = Course.objects.get(
        id=course_id
    )

    enrolled = Enrollment.objects.filter(

        user=request.user,

        course=course
    ).exists()

    if not enrolled:

        Enrollment.objects.create(

            user=request.user,

            course=course
        )

    return redirect(

        'course_lessons',

        course_id=course.id
    )
# =========================
# COURSE LESSONS
# =========================

# =========================
# COURSE LESSONS
# =========================

@login_required(login_url='login')

def course_lessons(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    enrollment = get_object_or_404(

        Enrollment,

        user=request.user,

        course=course
    )

    # =========================
    # UNLOCK SYSTEM
    # =========================

    days_passed = (
        date.today() - enrollment.enrolled_at
    ).days + 1

    lessons = Lesson.objects.filter(
        course=course
    ).order_by('day')

    # =========================
    # PROGRESS
    # =========================

    progress = int(
        (days_passed / course.total_days)
        * 100
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
        (lesson.day / lesson.course.total_days)
        * 100
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

    # =========================
    # QUIZ SUBMISSION
    # =========================

    if request.method == "POST":

        # Prevent multiple attempts

        if existing_attempt:

            score = existing_attempt.score

        else:

            correct_answers = 0

            total_questions = quiz_questions.count()

            for quiz in quiz_questions:

                selected_answer = request.POST.get(
                    f"quiz_{quiz.id}"
                )

                if selected_answer == quiz.correct_answer:

                    correct_answers += 1

            score = correct_answers

            # SAVE QUIZ ATTEMPT

            QuizAttempt.objects.create(

                user=request.user,

                lesson=lesson,

                score=score,

                total_questions=total_questions

            )

            # =========================
            # XP REWARD
            # =========================

            profile = UserProfile.objects.get(
                user=request.user
            )

            earned_xp = score * 10

            profile.xp += earned_xp

            profile.coins += score * 2

            profile.level = (
                profile.xp // 500
            ) + 1

            profile.save()

    context = {

        'lesson': lesson,

        'lessons': lessons,

        'quiz_questions': quiz_questions,

        'progress': progress,

        'days_passed': days_passed,

        'score': score,

        'existing_attempt': existing_attempt,

        'completed': completed

    }

    return render(
        request,
        'lesson_detail.html',
        context
    )
    
    
    # =========================
    # QUIZ SUBMISSION
    # =========================

    if request.method == "POST":

        if not existing_attempt:

            correct_answers = 0

            total_questions = quiz_questions.count()

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

            earned_xp = score * 50

            earned_coins = score * 10

            profile = UserProfile.objects.get(
                user=request.user
            )

            profile.xp += earned_xp

            profile.coins += earned_coins

            profile.level = (
                profile.xp // 500
            ) + 1

            profile.save()

        else:

            score = existing_attempt.score

    elif existing_attempt:

        score = existing_attempt.score

    profile = UserProfile.objects.get(
        user=request.user
    )

    completed = CompletedLesson.objects.filter(
        user=request.user,
        lesson=lesson
    ).exists()

    context = {

        'lesson': lesson,

        'lessons': lessons,

        'quiz_questions': quiz_questions,

        'progress': progress,

        'days_passed': days_passed,

        'score': score,

        'profile': profile,

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

        profile.level = (
            profile.xp // 500
        ) + 1

        profile.save()

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


@login_required(login_url='login')

def community(request):

    # CREATE POST

    if request.method == "POST":

        content = request.POST.get(
            'content'
        )

        if content:

            CommunityPost.objects.create(

                user=request.user,

                content=content

            )

    # FETCH POSTS

    posts = CommunityPost.objects.all().order_by(
        '-created_at'
    )

    # TOP USERS

    top_users = UserProfile.objects.all().order_by(
        '-xp'
    )[:5]

    # LIKED POSTS

    liked_posts = PostLike.objects.filter(
        user=request.user
    ).values_list(
        'post_id',
        flat=True
    )

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

    # Prevent incomplete users

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

        # SAVE COMPLETED LESSON

        CompletedLesson.objects.create(

            user=request.user,

            lesson=lesson
        )

        # GET USER PROFILE

        profile = UserProfile.objects.get(
            user=request.user
        )

        # XP + COINS

        profile.xp += 100

        profile.coins += 25

        profile.completed_lessons += 1

        profile.level = (
            profile.xp // 500
        ) + 1

        profile.save()

        # =========================
        # BADGES SYSTEM
        # =========================

        # FIRST LESSON

        if profile.completed_lessons == 1:

            Badge.objects.get_or_create(

                user=request.user,

                title='First Step',

                defaults={

                    'icon': '🚀',

                    'description':
                    'Completed first lesson'

                }

            )

        # 5 LESSONS

        if profile.completed_lessons == 5:

            Badge.objects.get_or_create(

                user=request.user,

                title='Fast Learner',

                defaults={

                    'icon': '⚡',

                    'description':
                    'Completed 5 lessons'

                }

            )

        # 10 LESSONS

        if profile.completed_lessons == 10:

            Badge.objects.get_or_create(

                user=request.user,

                title='Consistency King',

                defaults={

                    'icon': '🔥',

                    'description':
                    'Completed 10 lessons'

                }

            )

        # 1000 XP

        if profile.xp >= 1000:

            Badge.objects.get_or_create(

                user=request.user,

                title='1000 XP Club',

                defaults={

                    'icon': '💎',

                    'description':
                    'Reached 1000 XP'

                }

            )

    return redirect(
        'lesson_detail',
        lesson_id=lesson.id
    )
        
    # =========================
# LIKE POST
# =========================
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

    # UNLIKE

    if already_liked:

        already_liked.delete()

        post.likes -= 1

        if post.likes < 0:

            post.likes = 0

        post.save()

    # LIKE

    else:

        PostLike.objects.create(

            post=post,

            user=request.user
        )

        post.likes += 1

        post.save()

    return redirect(
        'community'
    )
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

        content = request.POST.get(
            'content'
        )

        if content:

            PostComment.objects.create(

                post=post,

                user=request.user,

                content=content

            )

    return redirect(
        'community'
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
        user=request.user
    )

    total_users = UserProfile.objects.count()

    rank = UserProfile.objects.filter(
        xp__gt=profile.xp
    ).count() + 1

    context = {

        'profile': profile,

        'badges': badges,

        'posts': posts,

        'certificates': certificates,

        'rank': rank,

        'total_users': total_users

    }

    return render(
        request,
        'profile.html',
        context
    )


import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# =========================
# PAYMENT PAGE
# =========================

@login_required(login_url='login')
def payment_page(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    # Check if already enrolled
    already_enrolled = Enrollment.objects.filter(
        user=request.user,
        course=course,
        is_paid=True
    ).exists()

    if already_enrolled:
        return redirect('course_lessons', course_id=course.id)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        "amount": 100,        # ₹1 in paise
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "course": course,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    }

    return render(request, 'payment.html', context)


# =========================
# PAYMENT SUCCESS
# =========================
import hmac
import hashlib

@csrf_exempt
@login_required(login_url='login')
def payment_success(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')

    # =========================
    # VERIFY SIGNATURE
    # =========================

    try:

        key_secret = settings.RAZORPAY_KEY_SECRET

        msg = f"{order_id}|{payment_id}"

        generated_signature = hmac.new(
            key_secret.encode(),
            msg.encode(),
            hashlib.sha256
        ).hexdigest()

        if generated_signature != signature:
            return render(request, 'payment_failed.html')

    except Exception as e:

        print(e)

    # =========================
    # SAVE ENROLLMENT
    # =========================

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    enrollment.is_paid = True
    enrollment.payment_id = payment_id
    enrollment.save()

    return redirect('course_lessons', course_id=course.id)