from django.db import models
from django.contrib.auth.models import User
import random
import string


# =========================
# REFERRAL PROFILE
# =========================

class ReferralProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    referral_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    referred_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='joined_users'
    )

    referral_count = models.IntegerField(
        default=0
    )

    earned_amount = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username