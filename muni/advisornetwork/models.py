from django.db import models

class Delegate(models.Model):
    name = models.CharField(max_length=500)
    position = models.CharField(max_length=500)
    committee = models.CharField(max_length=500)
    hotel_room_number = models.CharField(max_length=500)

class Advisor(models.Model):
    name = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    work_phone_number = models.CharField(max_length=20)
    mobile_phone_number = models.CharField(max_length=20)


