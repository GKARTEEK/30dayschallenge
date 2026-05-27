from django.contrib import admin

from .models import ReferralProfile


# =========================
# REFERRAL PROFILE ADMIN
# =========================

@admin.register(ReferralProfile)

class ReferralProfileAdmin(admin.ModelAdmin):

    list_display = (

        'user',

        'referral_code',

        'referred_by',

        'referral_count',

        'earned_amount',

        'created_at'
    )

    search_fields = (

        'user__username',

        'referral_code'
    )