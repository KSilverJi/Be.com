from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q # OR문 추가

from .models import Mate, MatePhoto, MateQuest, MateMsg
from myprofile.models import MyProfile
from django.contrib.auth.models import User

# Create your views here.
def mate_home(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    photos = MatePhoto.objects.filter(mate=mate)
    quests = MateQuest.objects.get(mate=mate)
    quest_done_num = quest_percent(quests)
    quest_done_per = round(quest_done_num/12*100)

    item={
        'mate' : mate,
        'photos' : photos,
        'quests' : quests,
        'quest_done_per' : quest_done_per,
    }
    return render(request, 'mate/mate.html', item)

def gallery(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    photos = MatePhoto.objects.filter(mate=mate)
    return render(request, 'mate/gallery.html', {'photos':photos})

def upload(request): #intimacy 다시 계산하여 저장한다.
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

def quest(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    quests = MateQuest.objects.get(mate=mate)
    quest_done_num = quest_percent(quests)
    quest_done_per = round(quest_done_num/12*100)

    item={
        'quests': quests,
        'quest_done_num' : quest_done_num,
        'quest_done_per' : quest_done_per,
    }
    #new = Task()
    #new.mate = mate
    #new.task = [0, 0, 0, 0, 0, 0, 0, 0]
    #new.save()
    return render(request, 'mate/quest.html', item)

def quest_done(request, quest_id): #intimacy 다시 계산하여 저장
    user = request.user
    profile = MyProfile.objects.get(username=user)
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    quests = MateQuest.objects.get(mate=mate)
    find_quest(quest_id, quests)
    return redirect('/mate/quest')

def find_quest(quest_id, quests):
    if quest_id==1:
        quests.quest1 = 1
    elif quest_id==2:
        quests.quest2 = 1
    elif quest_id==3:
        quests.quest3 = 1
    elif quest_id==4:
        quests.quest4 = 1
    elif quest_id==5:
        quests.quest5 = 1
    elif quest_id==6:
        quests.quest6 = 1
    elif quest_id==7:
        quests.quest7 = 1
    elif quest_id==8:
        quests.quest8 = 1
    elif quest_id==9:
        quests.quest9 = 1
    elif quest_id==10:
        quests.quest10 = 1
    elif quest_id==11:
        quests.quest11 = 1
    elif quest_id==12:
        quests.quest12 = 1
    
    quests.save()

def quest_percent(quests):
    quest_done_num = 0
    if quests.quest1==1:
        quest_done_num += 1
    if quests.quest2==1:
        quest_done_num += 1
    if quests.quest3==1:
        quest_done_num += 1
    if quests.quest4==1:
        quest_done_num += 1
    if quests.quest5==1:
        quest_done_num += 1
    if quests.quest6==1:
        quest_done_num += 1
    if quests.quest7==1:
        quest_done_num += 1
    if quests.quest8==1:
        quest_done_num += 1
    if quests.quest9==1:
        quest_done_num += 1
    if quests.quest10==1:
        quest_done_num += 1
    if quests.quest11==1:
        quest_done_num += 1
    if quests.quest12==1:
        quest_done_num += 1
    
    return quest_done_num