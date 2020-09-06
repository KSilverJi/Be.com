from django.shortcuts import render
from django.http import HttpResponse

from .models import MyProfile
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    user = request.user
    my = MyProfile.objects.get(username=user) # 현재 사용자의 프로필 정보를 불러온다.
    class_friends = MyProfile.objects.filter(school=my.school, school_year=my.school_year, school_class=my.school_class).exclude(username=user) # 같은 학교, 학년, 반인 친구들 프로필 정보
    # class_achievements = class_achievement(user)
    
    item={
        'my' : my,
        'class_friends' : class_friends,
        # 'class_achievements' : class_achievements,
    }
    return render(request, 'myprofile/myprofile.html', item)

def class_achievment(user): # user가 속한 학교/학년/반이 작성한 게시판 글 수 등 받아서 계산 -> DB에 업데이트, 활성도 점수 index 함수로 보내기.
    a = 1
    return a