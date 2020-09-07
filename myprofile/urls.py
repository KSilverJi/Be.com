from django.urls import path

from myprofile import views

app_name = 'myprofile'
urlpatterns = [
    path('', views.profile_home, name='home'),
    path('detail/<int:profile_id>', views.profile_detail, name='detail'),
    path('upload/', views.upload, name='upload'),
]

