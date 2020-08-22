from django.db import models
from django.contrib.auth.models import User

class MoodTracker(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE) # User 모델과 연결
    content = models.CharField(max_length=800) # 최대 800자
    published = models.DateTimeField(auto_now=True)
    mood = models.CharField(max_length=15)
    
    #timeout = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.username, self.published) # 유저와 날짜로 구분