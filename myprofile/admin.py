from django.contrib import admin
from myprofile.models import MyProfile, ProfilePhoto, MyClass

# Register your models here.
admin.site.register(MyProfile)
admin.site.register(ProfilePhoto)
admin.site.register(MyClass)