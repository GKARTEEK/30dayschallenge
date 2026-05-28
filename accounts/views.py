from django.shortcuts import render, redirect

from django.contrib.auth.models import User

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from .models import ReferralProfile


# =========================
# REGISTER
# =========================

def register_view(request):

    if request.method == 'POST':

        username = request.POST['username']

        email = request.POST['email']

        password = request.POST['password']

        referral_code = request.POST.get(
            'referral_code'
        )

        # =========================
        # CHECK USERNAME
        # =========================

        if User.objects.filter(
            username=username
        ).exists():

            return render(

                request,

                'register.html',

                {

                    'error':
                    'Username already exists'
                }
            )

        # =========================
        # CREATE USER
        # =========================

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password
        )

        user.save()

        # =========================
        # CREATE REFERRAL PROFILE
        # =========================

        profile = ReferralProfile.objects.create(

            user=user,

            referral_code=username.upper()
        )

        # =========================
        # HANDLE REFERRAL CODE
        # =========================

        if referral_code:

            try:

                referrer = ReferralProfile.objects.get(

                    referral_code=referral_code.upper()
                )

                profile.referred_by = referrer

                profile.save()

                referrer.referral_count += 1

                referrer.save()

            except Exception as e:

                print(e)

        return redirect('login')

    return render(
        request,
        'register.html'
    )


# =========================
# LOGIN
# =========================

def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(

            request,

            username=username,

            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

    return render(
        request,
        'login.html'
    )


# =========================
# LOGOUT
# =========================

def logout_view(request):

    logout(request)

    return redirect('home')


    