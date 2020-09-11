from django.urls import path

from . import views

app_name = 'mate' 
urlpatterns = [
    path('', views.mate_home, name="home"),
    path('gallery', views.gallery, name="gallery"),
    path('task', views.task, name="task"),
]

