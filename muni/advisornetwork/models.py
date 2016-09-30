from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class School(models.Model):
    name = models.CharField(max_length=500)
    address = models.TextField()
    phone_number = PhoneNumberField()
    delegate_count_estimate = models.IntegerField()
    transportation_required = models.BooleanField()
    interested_crisis_committees = models.BooleanField()
    interested_ipd_positions = models.BooleanField()
    top_three_positions = models.TextField(blank=True)
    user_account = models.OneToOneField(User)

    # MUNI trackin'
    paid_school_fee = models.BooleanField(default=False)
    paid_delegate_fees = models.BooleanField(default=False)


class Delegate(models.Model):
    name = models.CharField(max_length=500)
    position = models.CharField(max_length=500, blank=True)
    committee = models.CharField(max_length=500, blank=True)
    hotel_room_number = models.CharField(max_length=500, blank=True)
    school = models.ForeignKey(School)


class Advisor(models.Model):
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    work_phone_number = PhoneNumberField(blank=True)
    mobile_phone_number = PhoneNumberField()
    hotel_room_number = models.CharField(max_length=20, blank=True)
    school = models.ForeignKey(School)


