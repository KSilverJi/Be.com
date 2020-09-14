from django.urls import path

from mate import views

app_name = 'mate' 
urlpatterns = [
    path('', views.mate_home, name="home"),
    path('gallery', views.gallery, name="gallery"),
    path('quest', views.quest, name="quest"),
    path('questdone/<int:quest_id>', views.quest_done, name="quest-done"),
    path('upload/', views.upload, name='upload'),
	path('message/', views.send_message, name='send_message'),
]

