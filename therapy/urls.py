from django.urls import path
from . import views
import therapy.views

app_name = 'therapy'
urlpatterns = [
    path('', views.therapy, name='therapy'),
    path('result/', views.result, name='result')
]
