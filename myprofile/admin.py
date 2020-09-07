from django.contrib import admin
from myprofile.models import MyProfile, ProfilePhoto

# Register your models here.
admin.site.register(MyProfile)
admin.site.register(ProfilePhoto)