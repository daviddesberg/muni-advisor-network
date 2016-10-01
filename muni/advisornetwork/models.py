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
    additional_registration_notes = models.TextField(blank=True)

    marked_paid_at = models.DateTimeField(null=True, blank=True)  # for school fee
    marked_paid_transit_fee = models.DateTimeField(null=True, blank=True)
    marked_paid_delegate_fee = models.DateTimeField(null=True, blank=True)

    # MUNI trackin'
    paid_school_fee = models.BooleanField(default=False)
    paid_delegate_fees = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Delegate(models.Model):
    name = models.CharField(max_length=500)
    position = models.CharField(max_length=500, blank=True)
    committee = models.CharField(max_length=500, blank=True)
    hotel_room_number = models.CharField(max_length=500, blank=True)
    school = models.ForeignKey(School)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (School %s)" % (self.name, str(self.school))


class Advisor(models.Model):
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    work_phone_number = PhoneNumberField(blank=True)
    mobile_phone_number = PhoneNumberField()
    hotel_room_number = models.CharField(max_length=20, blank=True)
    school = models.ForeignKey(School)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (School %s)" % (self.name, str(self.school))
