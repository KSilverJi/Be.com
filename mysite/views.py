from django.views.generic import TemplateView
from django.views.generic import CreateView 
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy

from django.contrib.auth.mixins import AccessMixin
from django.views.defaults import permission_denied

from myprofile.models import MyProfile, MyClass
from moodtracker.models import MoodTracker, Wordcloud
from forum.models import Forum
from mate.models import Mate
from django.db.models import Q # OR문 추가
from therapy.models import Counsel

from django.shortcuts import render, redirect
from django.utils import timezone

from konlpy.tag import Okt
import nltk

from wordcloud import WordCloud
from wordcloud import STOPWORDS

from moodtracker.views import pos_neg_percent, mood_num, create_wordcloud, recent_mood_text, recent_pos_neg
from myprofile.views import class_achievement
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User


@login_required
def main(request):
    user = request.user
    profile = MyProfile.objects.get(username=user)
    class_friends = MyProfile.objects.filter(school=profile.school, school_year=profile.school_year, school_class=profile.school_class).exclude(username=user) # 같은 학교, 학년, 반인 친구들 프로필 정보
    # class_achievements = class_achievement(user)
    moodtrackers = MoodTracker.objects.filter(username=user) # 현재 사용자와 일치하는 정보만 불러온다
    pos_per, neg_per = pos_neg_percent(moodtrackers) # 긍정 부정 개수 구하기 (날짜 조건 걸어야 함)
    happy, sad, calm, angry, soso = mood_num(moodtrackers) # 감정 개수 구하기
    maxMood = find_max(happy, sad, calm, angry, soso)
    mft1, mft2, mft3 = create_wordcloud(moodtrackers, user) # 빈출 높은 단어 가져온다.
    wc = list_wordcloud(user)
    
    mate = list_mate(profile)
    year = timezone.datetime.now().year
    month = timezone.datetime.now().month
    day = timezone.datetime.now().day

    my_class = MyClass.objects.get(myschool=profile.school, hak=profile.school_year, ban=profile.school_class)
    class_score, class_score_text, class_level = class_achievement(my_class)

    forums = Forum.objects.order_by('-id')[:3]
    #forum_list = Forum.objects.all().order_by('-id')
    
    #page = request.GET.get('page')
    #posts = paginator.get_page(page)

    counsel = Counsel.objects.filter(teacher=user) #담당선생님이 현재 유저(선생님)와 같아야 한다.

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
        'mft1' : mft1,
        'mft2' : mft2,
        'mft3' : mft3,
        'maxMood' : maxMood,
        'class_score' : class_score,
        'class_score_text' : class_score_text,
        'class_level' : class_level,
        'forums':forums,
        'counsel':counsel,
    }
    return render(request, 'home.html', item)

def list_wordcloud(user):
    try:
        return Wordcloud.objects.get(username=user) # 워드 클라우드 객체 가져오기
    except Wordcloud.DoesNotExist:
        return None

def list_mate(profile):
    try:
        return Mate.objects.get(Q(mate1=profile) | Q(mate2=profile))
    except Mate.DoesNotExist:
        return None

def create_wordcloud(moodtrackers, user):  
    content_text = ''
    for record in moodtrackers:
        content_text = content_text + record.content
    
    okt = Okt()
    tokens_ko = okt.morphs(content_text)

    stopwords = ['나는', '나를', '내가', '너무', '없다', '정말', '것은', '있다.', '자꾸', '싶지', '않다', '같다', '싶다', '했다', '나왔다', '.', '이', '가', '을', '에', '를', '는', '들', '은', '이다', '것', '거', '에서', '했다', '다', '도', '하는', '만', '한테', '한', '수', '게', '랑', '한다', '하고', '?', '이랑', '싶다', '의', '으로',
              '요', '로', '으로', ',', ]

    tokens_ko = [each_word for each_word in tokens_ko
             if each_word not in stopwords]
    ko = nltk.Text(tokens_ko)
    most_freq_text = ko.vocab().most_common(3)

    if not most_freq_text:
        mft1 = '아직 없어요'
        mft2 = '감정일기를' 
        mft3 = '작성해주세요'
    else:
        mft1 = most_freq_text[0][0]
        mft2 = most_freq_text[1][0]
        mft3 = most_freq_text[2][0] 


    return mft1, mft2, mft3
    
def find_max(happy, sad, calm, angry, soso):
    maxValue = happy
    text = '행복해'
    if maxValue <= sad :
        maxValue = sad
        text = '슬퍼'
    elif maxValue <= calm :
        maxValue = calm
        text = '평온해'
    elif maxValue <= angry :
        maxValue = angry
        text = '화가 나'
    elif maxValue <= soso :
        maxValue = soso
        text = '그저 그래'
    
    if maxValue==0:
        text = '아직 없어요'

    return text

@login_required
def student_analysis(request, person_id):
    user = User.objects.get(id=person_id)
    moodtrackers = MoodTracker.objects.filter(username_id=person_id)

    rec_pos_per = recent_pos_neg(user)
    recent_mood, saying = recent_mood_text(rec_pos_per, user) # 요즘 기분 text, 명언 text
    pos_per, neg_per = pos_neg_percent(moodtrackers) # 긍정 부정 개수 구하기 (날짜 조건 걸어야 함)
    happy, sad, calm, angry, soso = mood_num(moodtrackers) # 감정 개수 구하기
    mft1, mft2, mft3 = create_wordcloud(moodtrackers, user) # 워드 클라우드 생성, 빈출 높은 단어 가져온다.
    wc = Wordcloud.objects.get(username=user) # 워드 클라우드 객체 가져오기

    item = {
        'pos_per' : pos_per,
        'neg_per' : neg_per,
        'happy' : happy,
        'sad' : sad,
        'calm' : calm,
        'angry' : angry,
        'soso' : soso,
        'wc' : wc,
        'moodtrackers' : moodtrackers,
        'user' : user,
        'mft1' : mft1,
        'mft2' : mft2,
        'mft3' : mft3,
        #'rec_pos_per' : rec_pos_per,
        'recent_mood' : recent_mood,
        #'rec_neg_per' : rec_neg_per,
        'saying' : saying,
    }

    return render(request, 'student_detail.html', item)

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

