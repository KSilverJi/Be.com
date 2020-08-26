from django.contrib import admin
from moodtracker.models import MoodTracker, Wordcloud

admin.site.register(MoodTracker)
admin.site.register(Wordcloud)