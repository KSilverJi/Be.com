from django.db import models

# Create your models here.
class Forum(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()
    images = models.ImageField(blank=True, upload_to="images", null=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]
