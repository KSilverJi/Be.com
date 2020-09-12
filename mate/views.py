from django.shortcuts import render, redirect
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
    tasks = MateTask.objects.get(mate=mate)
    task_done_num = task_percent(tasks)
    task_done_per = round(task_done_num/12*100)

    item={
        'mate' : mate,
        'photos' : photos,
        'tasks' : tasks,
        'task_done_per' : task_done_per,
    }
    return render(request, 'mate/mate.html', item)

def gallery(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    photos = MatePhoto.objects.filter(mate=mate)
    return render(request, 'mate/gallery.html', {'photos':photos})

def upload(request):
    if(request.method == 'POST'):
        user = request.user
        profile = MyProfile.objects.get(username=user)
        mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
        # name 속성이 imgs인 input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다 
        for img in request.FILES.getlist('imgs'):
            photo = MatePhoto() # ProfilePhoto 객체를 하나 생성한다.
            photo.mate = mate # 외래키로 현재 생성한 MyProfile의 기본키를 참조한다.
            photo.image = img # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            photo.save() # 데이터베이스에 저장
        return redirect('/mate/gallery')
    else:
        return render(request, 'mate/mate.html')

def task(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    tasks = MateTask.objects.get(mate=mate)
    task_done_num = task_percent(tasks)
    task_done_per = round(task_done_num/12*100)

    item={
        'tasks': tasks,
        'task_done_num' : task_done_num,
        'task_done_per' : task_done_per,
    }
    #new = Task()
    #new.mate = mate
    #new.task = [0, 0, 0, 0, 0, 0, 0, 0]
    #new.save()
    return render(request, 'mate/task.html', item)

def task_done(request, task_id):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    tasks = MateTask.objects.get(mate=mate)
    find_task(task_id, tasks)
    return redirect('/mate/task')

def find_task(task_id, tasks):
    if task_id==1:
        tasks.task1 = 1
    elif task_id==2:
        tasks.task2 = 1
    elif task_id==3:
        tasks.task3 = 1
    elif task_id==4:
        tasks.task4 = 1
    elif task_id==5:
        tasks.task5 = 1
    elif task_id==6:
        tasks.task6 = 1
    elif task_id==7:
        tasks.task7 = 1
    elif task_id==8:
        tasks.task8 = 1
    elif task_id==9:
        tasks.task9 = 1
    elif task_id==10:
        tasks.task10 = 1
    elif task_id==11:
        tasks.task11 = 1
    elif task_id==12:
        tasks.task12 = 1
    
    tasks.save()

def task_percent(tasks):
    task_done_num = 0
    if tasks.task1==1:
        task_done_num += 1
    if tasks.task2==1:
        task_done_num += 1
    if tasks.task3==1:
        task_done_num += 1
    if tasks.task4==1:
        task_done_num += 1
    if tasks.task5==1:
        task_done_num += 1
    if tasks.task6==1:
        task_done_num += 1
    if tasks.task7==1:
        task_done_num += 1
    if tasks.task8==1:
        task_done_num += 1
    if tasks.task9==1:
        task_done_num += 1
    if tasks.task10==1:
        task_done_num += 1
    if tasks.task11==1:
        task_done_num += 1
    if tasks.task12==1:
        task_done_num += 1
    
    return task_done_num