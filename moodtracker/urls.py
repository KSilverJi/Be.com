from django.urls import path

from moodtracker import views

app_name = 'moodtracker'
urlpatterns = [    
	path('', views.write_record),
	path('record/<int:record_id>', views.view_record, name='moodtracker_view_record'), 
	path('write/', views.write_record, name='moodtracker_write'),
    path('create/',views.create_record, name='create_record'),
    path('analysis/', views.analysis, name='moodtracker_analysis'),
]