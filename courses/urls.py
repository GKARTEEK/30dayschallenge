from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .views import (

    course_list,

    enroll_course,

    course_lessons,

    lesson_detail,

    complete_lesson,

    leaderboard,

    community,

    generate_certificate,

    like_post,

    add_comment,

    profile_page,

    payment_success,
    payment_page,

    about_page,
    contact_page,
    privacy_page,
    terms_page,
)


urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        '',
        course_list,
        name='home'
    ),

    # =========================
    # COURSES
    # =========================

    path(
        'courses/',
        course_list,
        name='courses'
    ),

    # =========================
    # ENROLL
    # =========================

    path(
        'enroll/<int:course_id>/',
        enroll_course,
        name='enroll_course'
    ),

    # =========================
    # LESSONS
    # =========================

    path(
        'my-learning/<int:course_id>/',
        course_lessons,
        name='course_lessons'
    ),

    # =========================
    # LESSON DETAIL
    # =========================

    path(
        'lesson/<int:lesson_id>/',
        lesson_detail,
        name='lesson_detail'
    ),

    # =========================
    # COMPLETE LESSON
    # =========================

    path(
        'complete-lesson/<int:lesson_id>/',
        complete_lesson,
        name='complete_lesson'
    ),

    # =========================
    # LEADERBOARD
    # =========================

    path(
        'leaderboard/',
        leaderboard,
        name='leaderboard'
    ),

    # =========================
    # COMMUNITY
    # =========================

    path(
        'community/',
        community,
        name='community'
    ),

    path(
    'certificate/<int:course_id>/',
    generate_certificate,
    name='generate_certificate'
    ),

    path(
    'like-post/<int:post_id>/',
    like_post,
    name='like_post'
),

path(
    'add-comment/<int:post_id>/',
    add_comment,
    name='add_comment'
),
path(
    'profile/',
    profile_page,
    name='profile'
),

path(
    'checkout/',
    payment_page,
    name='payment_page'
),

path(
    'payment-success/',
    payment_success,
    name='payment_success'
),


path(
    'about/',
    about_page,
    name='about'
),

path(
    'contact/',
    contact_page,
    name='contact'
),

path(
    'privacy-policy/',
    privacy_page,
    name='privacy'
),

path(
    'terms-and-conditions/',
    terms_page,
    name='terms'
),

]
