from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q # OR문 추가

from .models import Mate, MatePhoto, MateTask
from myprofile.models import MyProfile
from django.contrib.auth.models import User

# Create your views here.
def mate_home(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    photos = MatePhoto.objects.filter(mate=mate)
    task = MateTask.objects.get(mate=mate)

    item={
        'mate' : mate,
        'photos' : photos,
        'task' : task,
    }
    return render(request, 'mate/mate.html', item)

def gallery(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    photos = MatePhoto.objects.filter(mate=mate)
    return render(request, 'mate/gallery.html', {'photos':photos})

def task(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    tasks = MateTask.objects.get(mate=mate)
    return render(request, 'mate/task.html', {'tasks':tasks})