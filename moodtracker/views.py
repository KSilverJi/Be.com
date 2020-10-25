from django.shortcuts import render, redirect
from django.utils import timezone
import random

from django.views import generic

from .models import MoodTracker, Wordcloud
from django.contrib.auth.models import User

import pickle
from konlpy.tag import Okt
import nltk

from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt

import requests
from io import BytesIO
from PIL import Image, ImageDraw
import cognitive_face as CF

from django.contrib.auth.decorators import login_required

# 작성된 감정 일기 보는 화면으로 이동
@login_required
def view_record(request, record_id):
    user = request.user
    records = MoodTracker.objects.filter(username=user) # 유저의 모든 감정 일기 기록
    sp_record = MoodTracker.objects.get(pk=record_id) # 요청받은 감정 일기 1개

    

    item = {
        'records': records,
        'sp_record': sp_record,
    }
    return render(request, 'moodtracker/moodtracker_record.html', item)


# 인식된 얼굴에 네모 박스 그리는 함수 작성
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))



# 감정 일기 분석 화면으로 이동
@login_required
def analysis(request):
    user = request.user
    moodtrackers = MoodTracker.objects.filter(username=user) # 현재 사용자와 일치하는 정보만 불러온다
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
        #'rec_neg_per' : rec_neg_per,
        'recent_mood' : recent_mood,
        'saying' : saying,
    }

    return render(request, 'moodtracker/moodtracker_analysis.html', item)


# 감정 일기 쓰는 페이지로 이동
@login_required
def write_record(request):
    user = request.user
    records = MoodTracker.objects.filter(username=user)
    year = timezone.datetime.now().year
    month = timezone.datetime.now().month
    day = timezone.datetime.now().day
    item = {
        'records' : records,
        'year' : year,
        'month' : month,
        'day' : day,
    }
    return render(request, 'moodtracker/moodtracker_write.html', item)


# Analysis - 긍정, 부정 비율 구하기
def pos_neg_percent(moodtrackers):
    pos=neg=0

    for record in moodtrackers:
        if record.pos_neg == 0:
            neg+=1
        else:
            pos+=1
    
    if pos == 0:
        pos_per = 0 # 0일 경우 zero division error 방지
    else:
        pos_per = round(pos/(pos+neg)*100, 1) # XX.X% 반환
    
    if neg == 0:
        neg_per = 0 # 0일 경우 zero division error 방지
    else:
        neg_per = round(neg/(pos+neg)*100, 1) # XX.X% 반환

    return pos_per, neg_per

# Analysis - 최근 10개 일기의 긍정, 부정 비율
def recent_pos_neg(user):
    recent_ten = MoodTracker.objects.filter(username=user).order_by("-id")[:7]
    pos=neg=0 # 10개 미만일 때 총 개수 세기 위해 neg도 센다.
    for record in recent_ten:
        if record.pos_neg == 1:
            pos+=1
        else:
            neg+=1
    
    if pos == 0:
        pos_per = 0 # 0일 경우 zero division error 방지
    else:
        pos_per = round(pos/(pos+neg)*100, 1) # XX.X% 반환
    
    return pos_per

# Analysis - 요즘 기분 text, 명언 text
def recent_mood_text(rec_pos_per, user):
    if rec_pos_per >= 0 and rec_pos_per <= 20 :
        text = '요즘 스트레스를 받는 일이 있나요? 혹시 우울감을 느낀다면 선생님이나 전문가에게 도움을 받아보는 건 어떨까요?'
        saying = '길을 잃는 다는 것은 곧 길을 알게 된다는 것이다. –동아프리카속담'
    elif rec_pos_per <= 40 :
        text = '요즘 기분이 상할 만한 일이 있었나 봐요. 친구들과의 대화, 혼자만의 시간, 상담 등을 통해 몸과 마음을 재충전하는 걸 추천해 드려요.'
        saying = '겨울이 오면 봄이 멀지 않으리. -셸리'
    elif rec_pos_per <= 60 :
        text = '기분이 좋았던 날도, 안 좋았던 날도 있었네요. '+str(user)+'님의 하루가 매일매일 즐겁길 바래요!'
        saying = '만족하게 살고 때때로 웃으며 많은 사람을 사랑한 삶이 성공한다. - 스탠리'
    elif rec_pos_per <= 80 : 
        text = str(user)+'님의 요즘은 좋은 일이 많았군요! 앞으로 속상한 일이 생겨도 '+str(user)+'님은 잘 헤쳐나갈 수 있을 거예요. 그렇지만 도움이 필요하다면 언제든지 말해주세요.'
        saying = '오랫동안 꿈을 그리는 사람은 마침내 그 꿈을 닮아 간다. -앙드레 말로'
    elif rec_pos_per <= 100 : 
        text = '긍정의 기운이 가득한 요즘! 만족스러운 일상을 보내고 있나요? '+str(user)+'님의 일상이 더욱 즐거운 일들로 가득했으면 좋겠어요. 도움이 필요하다면 언제든지 말해주세요.'
        saying = '언제나 현재에 집중할 수 있다면 행복할 것이다. -파울로 코엘료'
    else:
        text = '텍스트 불러오기 오류'
        saying = '명언 불러오기 오류'
    return text, saying

# Analysis - 감정 개수 구하기
def mood_num(moodtrackers):
    happy=sad=calm=angry=soso = 0

    for record in moodtrackers:
        if record.mood == 'happy':
            happy+=1
        elif record.mood == 'sad':
            sad+=1
        elif record.mood == 'calm':
            calm+=1
        elif record.mood == 'angry':
            angry+=1
        else :
            soso+=1
    return happy, sad, calm, angry, soso

# Analysis - 워드 클라우드 생성
def create_wordcloud(moodtrackers, user):
    # 이전 워드클라우드 모델에서 삭제
    instance = Wordcloud.objects.filter(username=user) 
    instance.delete()
    
    content_text = ''
    for record in moodtrackers:
        content_text = content_text + record.content
    
    okt = Okt()
    tokens_ko = okt.morphs(content_text)

    stopwords = ['안', '나', '내', '나는', '나를', '내가', '너무', '없다', '정말', '것은', '있다.', '자꾸', '싶지', '않다', '같다', '싶다', '했다', '나왔다', '.', '이', '가', '을', '에', '를', '는', '들', '은', '이다', '것', '거', '에서', '했다', '다', '도', '하는', '만', '한테', '한', '수', '게', '랑', '한다', '하고', '?', '이랑', '싶다', '의', '으로',
              '요', '로', '으로', ',', ]

    tokens_ko = [each_word for each_word in tokens_ko
             if each_word not in stopwords]
    ko = nltk.Text(tokens_ko)
    most_freq_text = ko.vocab().most_common(3)

    wordcloud = WordCloud(font_path='moodtracker/static/fonts/AppleSDGothicNeoSB.ttf', background_color='white', stopwords=stopwords, width=500, height=500).generate_from_text(content_text)
    filename1 = 'media/%s_wc.png' % user
    filename2 = '%s_wc.png' % user 
    wordcloud.to_file(filename1)
    '''
    plt.figure(figsize=(400,400)) #이미지 사이즈 지정
    plt.imshow(wordcloud)
    plt.axis("off") #x y 축 숫자 제거
    plt.show()
    '''
    wc = Wordcloud() # 워드클라우드 객체 하나 생성
    wc.username = user 
    wc.wc_image = filename2 
    wc.save() # 데이터베이스에 저장

    mft1 = most_freq_text[0][0]
    mft2 = most_freq_text[1][0]
    mft3 = most_freq_text[2][0] 
    return mft1, mft2, mft3


def tokenizer(text):
    okt = Okt()
    return okt.morphs(text)

# 작성 내용을 모델에 돌려서 긍정/부정 결과 얻는다.
# !!계속 오류나는 중.
def use_model(content):
    with open('static/pipe.dat', 'rb') as fp:
        pipe = pickle.load(fp)
    
    import numpy as np

    str = [content]
    #r1 = np.max(pipe.predict_proba(str)*100) # 예측 정확도
    r2 = pipe.predict(str)[0] # 예측 결과

    if r2 == '1' :
        pos_neg = 1 # 긍정
    else :
        pos_neg = 0 # 부정
    
    return pos_neg


# MoodTracker 일기 내용 저장 & 긍정부정 모델 돌려서 결과 같이 저장
def create_record(request):
    user = request.user

    year = timezone.datetime.now().year
    month = timezone.datetime.now().month
    day = timezone.datetime.now().day

    content = request.POST['content']

    mood_record = MoodTracker()
    mood_record.username = user
    mood_record.content = content
    mood_record.mood = request.POST['mood'] 
    mood_record.pub_date = timezone.datetime.now()
    mood_record.pub_date_year = year
    mood_record.pub_date_month = month
    mood_record.pub_date_day = day

    images = request.FILES['images']
    
    emotion = {}

    emotion = find_emotion(images, user, year, month, day) # 해당 감정 일기
    emotion = emotion[0]
    mood_record.anger = round(emotion['emotion']['anger']*100, 1)
    mood_record.contempt = round(emotion['emotion']['contempt']*100, 1)
    mood_record.disgust = round(emotion['emotion']['disgust']*100, 1)
    mood_record.fear = round(emotion['emotion']['fear']*100, 1)
    mood_record.happiness = round(emotion['emotion']['happiness']*100, 1)
    mood_record.neutral = round(emotion['emotion']['neutral']*100, 1)
    mood_record.sadness = round(emotion['emotion']['sadness']*100, 1)
    mood_record.surprise = round(emotion['emotion']['surprise']*100, 1)
    
    filename2 = '%s_face_%s_%s_%s.png' % (user, year, month, day)

    mood_record.images = filename2

    pos_neg = use_model(content)
    mood_record.pos_neg = pos_neg    

    mood_record.save()
    return redirect('/moodtracker/record/'+str(mood_record.id)) # '/moodtracker/' + +str(mood_record.id)

def find_emotion(images, user, year, month, day):
    KEY = '66b40727db3b42b2a07497598b032d19' # 자신의 Cognitive Services API KEY
    CF.Key.set(KEY)

    BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/' # 자신의 지역에 해당하는 URL
    CF.BaseUrl.set(BASE_URL)

    img_url = images #'face_image.jpg' # 이미지 파일의 경로
    faces = CF.face.detect(img_url,True,False,'emotion') # 중요!
    # detect 함수는 4가지의 매개변수를 갖는다.
    # 첫 번째 인자 : 이미지파일
    # 두 번째 인자 : face_id의 반환 여부
    # 세 번째 인자 : landmarks(눈,코,입 등의 위치)의 반환 여부
    # 네 번째 인자 : 반환할 속성(연령,성별 등)
    emotion = []
    for face in faces:
        emotion.append(face['faceAttributes']) # 터미널 창에 속성값들을 출력

    img = Image.open(img_url) # img 변수에 이미지 파일을 넣어준다.
    draw = ImageDraw.Draw(img)
    for face in faces:
        draw.rectangle(getRectangle(face), outline='red', width=2) # 인식된 얼굴들에 네모 박스 쳐주기
    
    filename1 = 'media/%s_face_%s_%s_%s.png' % (user, year, month, day)
    img.save(filename1)

    return emotion
