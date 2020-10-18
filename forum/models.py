from django.db import models
from django.contrib.auth.models import User
from myprofile.models import MyProfile, MyClass

# Create your models here.
class Forum(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()
    images = models.ImageField(blank=True, upload_to="images", null=True)
    #추가
    writer = models.ForeignKey(MyProfile, on_delete=models.CASCADE, verbose_name='USERNAME', blank=True, null=True, related_name='writer')
    #ForeignKey(User, verbose_name = "작성자", on_delete = models.CASCADE)


    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

