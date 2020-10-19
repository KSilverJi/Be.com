from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import MyProfile, ProfilePhoto, MyClass
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

@login_required
def profile_home(request):
    user = request.user
    my = MyProfile.objects.get(username=user) # 현재 사용자의 프로필 정보를 불러온다.
    class_friends = MyProfile.objects.filter(school=my.school, school_year=my.school_year, school_class=my.school_class).exclude(username=user) # 같은 학교, 학년, 반인 친구들 프로필 정보
    my_class = MyClass.objects.get(myschool=my.school, hak=my.school_year, ban=my.school_class)
    class_score, class_score_text, class_level = class_achievement(my_class) # 학급 활성도
    
    item={
        'my' : my,
        'class_friends' : class_friends,
        'class_score' : class_score,
        'class_score_text' : class_score_text,
        'class_level' : class_level,
    }
    return render(request, 'myprofile/myprofile.html', item)

def class_achievement(my_class): # user가 속한 학교/학년/반이 작성한 게시판 글 수 등 받아서 계산 -> DB에 업데이트, 활성도 점수 index 함수로 보내기.
    a = my_class.class_intimacy
    if a >= 0 and a <= 20 :
        class_score_text = str(my_class.hak)+'학년 '+str(my_class.ban)+'반의 새싹이 피어났어요! 반 친구들과 함께 키워보아요!'
        class_level = 1
    elif a <= 40 :
        class_score_text = '벌써 이만큼 자랐네요! 나무가 될 때까지 더 키워볼까요?'
        class_level = 2
    elif a <= 60 :
        class_score_text = str(my_class.hak)+'학년 '+str(my_class.ban)+'반과 함께 무럭무럭 자라고 있어요! 잎이 많아질 때까지 조금 더 힘내볼까요?'
        class_level = 3
    elif a <= 80 :
        class_score_text = '우와, 나무가 정말 많이 자랐어요! 조만간 꽃이 피겠는걸요?'
        class_level = 4
    elif a <= 100 :
        class_score_text = '짝짝짝! '+str(my_class.hak)+'학년 '+str(my_class.ban)+'반의 활발한 소통이 꽃을 피웠어요!'
        class_level = 5 
    return a, class_score_text, class_level

@login_required
def profile_detail(request, profile_id):
    user = request.user # 현재 로그인한 사용자
    person = MyProfile.objects.get(pk=profile_id) # 보여줄 프로필의 주인
    person_images = ProfilePhoto.objects.filter(myprofile=person) # 프로필 주인이 올린 사진들
    
    if person.username==user : # 내 프로필일 때
        detail = 'my'
    else: # 다른 친구 프로필일 때
        detail = 'friend'
    
    # 이미지 모델에서 person.username으로 필터해온다.
    class_friends = MyProfile.objects.filter(school=person.school, school_year=person.school_year, school_class=person.school_class).exclude(username=user) # 같은 학교, 학년, 반인 친구들 프로필 정보

    item = {
        'person' : person,
        'person_images' : person_images,
        'detail' : detail,
        'class_friends' : class_friends,
    }
    return render(request, 'myprofile/profile_detail.html', item)

def upload(request):
    if(request.method == 'POST'):
        user = request.user
        user_id = MyProfile.objects.get(username=user)
        # name 속성이 imgs인 input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다 
        for img in request.FILES.getlist('imgs'):
            photo = ProfilePhoto() # ProfilePhoto 객체를 하나 생성한다.
            photo.myprofile = user_id # 외래키로 현재 생성한 MyProfile의 기본키를 참조한다.
            photo.image = img # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            photo.topic = request.POST.get('topic')
            photo.save() # 데이터베이스에 저장
        return redirect('/myprofile/detail/' + str(user_id.id))
    else:
        return render(request, 'myprofile/myprofile.html')