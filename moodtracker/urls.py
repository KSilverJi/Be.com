from django.urls import path

from moodtracker import views

app_name = 'moodtracker'
urlpatterns = [    
	path('', views.write_record, name='home'),
	path('record/<int:record_id>', views.view_record, name='view'), 
	path('write/', views.write_record, name='write'),
    path('create/',views.create_record, name='create'),
    path('analysis/', views.analysis, name='analysis'),
]