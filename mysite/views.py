from django.views.generic import TemplateView
from django.views.generic import CreateView 
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy

from django.contrib.auth.mixins import AccessMixin
from django.views.defaults import permission_denied

from myprofile.models import MyProfile
from moodtracker.models import MoodTracker, Wordcloud
from mate.models import Mate
from django.db.models import Q # OR문 추가

from django.shortcuts import render, redirect
from django.utils import timezone

from moodtracker.views import pos_neg_percent, mood_num, create_wordcloud

def test(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    class_friends = MyProfile.objects.filter(school=profile.school, school_year=profile.school_year, school_class=profile.school_class).exclude(username=user) # 같은 학교, 학년, 반인 친구들 프로필 정보
    # class_achievements = class_achievement(user)
    moodtrackers = MoodTracker.objects.filter(username=user) # 현재 사용자와 일치하는 정보만 불러온다
    pos_per, neg_per = pos_neg_percent(moodtrackers) # 긍정 부정 개수 구하기 (날짜 조건 걸어야 함)
    happy, sad, calm, angry, soso = mood_num(moodtrackers) # 감정 개수 구하기
    # create_wordcloud(moodtrackers, user) # 워드 클라우드 생성
    wc = Wordcloud.objects.get(username=user) # 워드 클라우드 객체 가져오기
    mate = Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    year = timezone.datetime.now().year
    month = timezone.datetime.now().month
    day = timezone.datetime.now().day

    item={
        'profile' : profile,
        'class_friends' : class_friends,
        'happy' : happy,
        'sad' : sad,
        'calm' : calm,
        'angry' : angry,
        'soso' : soso,
        'wc' : wc,
        'moodtrackers' : moodtrackers,
        'mate' : mate,
        'year' : year,
        'month' : month,
        'day' : day,
        # 'class_achievements' : class_achievements,
    }
    return render(request, 'home.html', item)

    
#--- Homepage
class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user
        my = MyProfile.objects.get(username=user)
        context['contents'] = {my.school, my.school_year}
        # context['apps'] = ['myprofile', 'moodtracker', 'mate']
        return context



#--- User Creation
class UserCreateView(CreateView): 
    template_name = 'registration/register.html' 
    form_class = UserCreationForm 
    success_url = reverse_lazy('register_done') 


class UserCreateDoneTV(TemplateView): 
    template_name = 'registration/register_done.html'


class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.owner:
            self.handle_no_permission()
        return super().get(request, *args, **kwargs)

