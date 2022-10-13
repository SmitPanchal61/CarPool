from django.db import models
from email import message
from django.conf import settings
import datetime

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=90)
    email = models.EmailField(max_length=90)
    message = models.TextField()

class userInfo(models.Model):
    firstname = models.CharField(max_length=90)
    lastname = models.CharField(max_length=90)
    email = models.EmailField()
    mobile = models.IntegerField()
    gender = models.TextField()
    dob = models.DateField()
    address = models.CharField(max_length=500)
    pin = models.IntegerField()
    drivelic = models.CharField(max_length=90)
    drivelicpic = models.FileField()
    user_id = models.IntegerField()
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class userCarpools(models.Model):
    start = models.CharField(max_length=90)
    to = models.CharField(max_length=90)
    poolDate = models.DateField(default=datetime.date.today)
    poolTime = models.TimeField(default=datetime.time)
    brand = models.TextField()
    carNo = models.TextField(max_length=10)
    price = models.IntegerField(default=0)
    color = models.TextField()
    user_id = models.IntegerField()