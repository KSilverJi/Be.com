from django.db import models
from django.contrib.auth.models import User
from myprofile.models import MyProfile, MyClass

# Create your models here.
class Counsel(models.Model):
    username = models.CharField(max_length=10, blank=True, null=True)
    who = models.CharField(max_length=10)
    how = models.CharField(max_length=10)
    teacher = models.CharField(max_length=10)
    about = models.CharField(max_length=20)
    detailtext = models.TextField()
    datenum = models.CharField(max_length=20)
    timepick = models.CharField(max_length=20)
