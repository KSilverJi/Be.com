from django.urls import path
from . import views
import forum.views

urlpatterns = [
    path('', forum.views.home, name='home'),
    #path('list/',views.home,name='home'),
    path('new/', views.new, name='new'),
    path('detail/<int:forum_id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('postcreate/', views.postcreate, name='postcreate'),
    path('update/<int:forum_id>/', views.update, name='update'),
    path('delete/<int:forum_id>/', views.delete, name='delete'),
    path('search', views.search, name='search'),
]
