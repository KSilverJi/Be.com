from django.urls import path

from myprofile import views

app_name = 'myprofile'
urlpatterns = [
    path('', views.index, name='home'),
]

