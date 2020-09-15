from django.db import models
from django.db.models import IntegerField
from django.contrib.postgres.fields import ArrayField
#from django.contrib.auth.models import User
from myprofile.models import MyProfile
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.


class Mate(models.Model):
    mate1 = models.ForeignKey(MyProfile, on_delete=models.CASCADE, verbose_name='USERNAME', blank=True, null=True, related_name='mate1') # 학생1의 id (User 모델과 연결)
    mate2 = models.ForeignKey(MyProfile, on_delete=models.CASCADE, verbose_name='USERNAME', blank=True, null=True, related_name='mate2') # 학생2의 id (User 모델과 연결)
    intimacy = models.IntegerField(default=0) # Quest 3%, Photo 1%, Message 1% 증가
    
    def __str__(self):
        return "%s - %s" % (self.mate1, self.mate2)

class MatePhoto(models.Model):
    mate = models.ForeignKey(Mate, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='', blank=True, null=True)

    def __str__(self):
        return "%s" % self.mate

class MateQuest(models.Model): # 0이 완료 안 된 상태
    mate = models.ForeignKey(Mate, on_delete=models.CASCADE, null=True) # Mate 모델과 연결
    quest1 = models.IntegerField(default=0)
    quest2 = models.IntegerField(default=0)
    quest3 = models.IntegerField(default=0)
    quest4 = models.IntegerField(default=0)
    quest5 = models.IntegerField(default=0)
    quest6 = models.IntegerField(default=0)
    quest7 = models.IntegerField(default=0)
    quest8 = models.IntegerField(default=0)
    quest9 = models.IntegerField(default=0)
    quest10 = models.IntegerField(default=0)
    quest11 = models.IntegerField(default=0)
    quest12 = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.mate

class MateMsg(models.Model):
    mate = models.ForeignKey(Mate, on_delete=models.CASCADE, null=True) # Mate 모델과 연결
    sender = models.ForeignKey(MyProfile, on_delete=models.CASCADE, verbose_name='USERNAME', blank=True, null=True)
    content = models.CharField(max_length=400)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

    @property
    def created_string(self): # time 변수에 현재시간에서 작성시간을 뺀 작성경과 시간을 저장
        time = datetime.now(tz=timezone.utc) - self.created_date

        if time < timedelta(minutes=1): # timedelta 메소드를 사용하여 분, 시간, 일 단위로 표시
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_date.date()
            return str(time.days) + '일 전'
        else:
            return False # 7일이 지날 경우 false를 반환하여 템플릿에서 원래의 Date형식으로 표시

#class Task(models.Model):
#    mate = models.ForeignKey(Mate, on_delete=models.CASCADE, null=True) # Mate 모델과 연결
#    task = ArrayField(IntegerField(), size=8)