from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=500)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    delegate_count_estimate = models.IntegerField()
    transportation_required = models.BooleanField()
    interested_crisis_committees = models.BooleanField()
    interested_ipd_positions = models.BooleanField()
    top_three_positions = models.TextField(blank=True)
    user_account = models.OneToOneField(User)


