from django.db import models
from django.contrib.auth.models import User

class MyProfile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='USERNAME', blank=True, null=True) # User 모델과 연결
    school = models.CharField(max_length=20)
    school_year = models.IntegerField(default=0)
    school_class = models.IntegerField(default=0)
    intro = models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='', default='default.png')

    def __str__(self):
        return "%s" % self.username # 유저 이름으로 구분
    
class ProfilePhoto(models.Model):
    myprofile = models.ForeignKey(MyProfile, on_delete=models.CASCADE, null=True)
    topic = models.CharField(max_length=30, default=0, null=True)
    image = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.myprofile, self.id)


class MyClass(models.Model):
    #myprofile = models.ForeignKey(MyProfile, on_delete=models.CASCADE, null=True)
    myschool=models.CharField(max_length=20)
    hak = models.IntegerField(default=2)
    ban = models.IntegerField(default=6)
    class_intimacy=models.IntegerField(default=0)