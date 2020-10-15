from django.db import models
from django.contrib.auth.models import User

class MoodTracker(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='USERNAME', blank=True, null=True) # User 모델과 연결
    content = models.CharField(max_length=800) # 최대 800자
    pub_date = models.DateTimeField(auto_now=True)
    pub_date_year = models.CharField(max_length=10, default=0)
    pub_date_month = models.CharField(max_length=10, default=0)
    pub_date_day = models.CharField(max_length=10, default=0)
    mood = models.CharField(max_length=15)
    pos_neg = models.IntegerField(default=0)
    
    images = models.ImageField(blank=True, upload_to="images", null=True)
    anger = models.FloatField(default=0)
    contempt = models.FloatField(default=0)
    disgust = models.FloatField(default=0)
    fear = models.FloatField(default=0)
    happiness = models.FloatField(default=0)
    neutral = models.FloatField(default=0)
    sadness = models.FloatField(default=0)
    surprise = models.FloatField(default=0)
    #timeout = models.IntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.username, self.pub_date) # 유저와 날짜로 구분

class Wordcloud(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='USERNAME', blank=True, null=True)
    wc_image = models.ImageField(upload_to='')


    '''
        테스트 데이터
        자꾸 짜증나게 말을 하는 친구가 있다. 우리 반 대신 다른 반으로 가고 싶다. 담임 선생님이 나를 안좋아한다. 담임이 자꾸 나만 혼낸다. 담임이 성적 떨어졌다고 혼냈다. 담임이 교무실에서 혼냈다.
        부정적인 리뷰
        정확도 : 90.238
        angry

        엄마랑 오랜만에 쇼핑을 가서 옷도 사고 신발도 샀다. 공부로부터 벗어나서 재밌게 노니까 행복했다.
        긍정적인 리뷰
        정확도 : 95.094
        happy

        야자를 땡땡이 치려다가 선생님한테 걸려서 혼났다. 떡볶이가 너무 땡겼는데...
        부정적인 리뷰
        정확도 : 53.908
        sad

        자전거를 타고 한강 주변을 돌았다. 날씨가 습해서 개운하진 않았다. 집에 와서 샤워하고 아빠가 사오신 딸기우유를 마셨다.
        긍정적인 리뷰
        정확도 : 84.671
        soso

        카페에서 내가 좋아하는 오레오 케이크를 먹으며 공부하고 친구들과 수다떨었다. 사실 공부는 많이 안 했지만 스트레스가 풀렸다.
        긍정적인 리뷰
        정확도 : 92.208
        calm
    '''
