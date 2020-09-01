from django.shortcuts import render
from django.utils import timezone

from django.views import generic

from .models import MoodTracker, Wordcloud
from django.contrib.auth.models import User

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt

from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt

#형태소로 쪼개는 함수
def tokenizer(text):
    okt = Okt()
    return okt.morphs(text)


#평점 전처리 함수
def pos_neg_preprocessing(value):
    if value==0 :
        return '0'
    else :
        return '1'



# 전처리, 데이터 준비
def step1_data_preprocessing(content):
    # 수집한 데이터를 읽어온다.
    df = content

    # 전처리를 수행한다
    df['rating'] = df['rating'].apply(pos_neg_preprocessing)

    # 학습데이터와 테스트 데이터로 나눈다.
    text_list = df['sentences'].tolist()
    pos_neg_list = df['rating'].tolist()

    # 80%는 학습, 20%는 test data
    text_train, text_test, pos_neg_train, pos_neg_test = train_test_split(text_list, pos_neg_list, test_size=0.3, random_state=123, shuffle=True)

    return text_train, text_test, pos_neg_train, pos_neg_test

# 학습
def step2_learning(X_train, y_train, X_test, y_test):
    #주어진 데이터를 단어 사전으로 만들고 각 단어의 빈도수를 계산한 후 벡터화하는 객체 생성
    tfidf = TfidfVectorizer(lowercase=False, tokenizer=tokenizer)

    # 문장별 나오는 단어 수 세서 수치화, 벡터화해서 학습 시킨다.
    logistic = LogisticRegression(C=10.0, penalty='l2', random_state=0)

    pipe=Pipeline([('vect', tfidf), ('clf', logistic)])

    #학습한다.
    pipe.fit(X_train, y_train)

    #학습 정확도 측정
    y_pred = pipe.predict(X_test)
    print('학습 정확도: ', accuracy_score(y_test, y_pred))

    #학습된 모델을 저장한다.
    with open('./static/pipe.dat', 'wb') as fp:
        pickle.dump(pipe, fp)

    print('모델 저장 완료')


# 학습 함수
def learning():
    text_train, text_test, pos_neg_train, pos_neg_test = step1_data_preprocessing()
    step2_learning(text_train, pos_neg_train, text_test, pos_neg_test)

# 감정 일기 보는 화면으로 이동
def view_record(request):
    return render(request, 'moodtracker/moodtracker_record.html')


# 감정 일기 분석 화면으로 이동
def analysis(request):
    user = request.user
    moodtrackers = MoodTracker.objects.filter(username=user) # 현재 사용자와 일치하는 정보만 불러온다
 
    pos_per, neg_per = pos_neg_percent(moodtrackers) # 긍정 부정 개수 구하기 (날짜 조건 걸어야 함)
    happy, sad, calm, angry, soso = mood_num(moodtrackers) # 감정 개수 구하기
    create_wordcloud(moodtrackers, user) # 워드 클라우드 생성
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
    }

    return render(request, 'moodtracker/moodtracker_analysis.html', item)


# 감정 일기 쓰는 페이지로 이동
def write_record(request):
    return render(request, 'moodtracker/moodtracker_write.html')


# Analysis - 긍정, 부정 비율 구하기
def pos_neg_percent(moodtrackers):
    pos=neg=0

    # 날짜 조건 걸어야 함
    for record in moodtrackers:
        if record.pos_neg == 0:
            neg+=1
        else:
            pos+=1
    return pos/(pos+neg)*100, neg/(pos+neg)*100
    

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

    stopwords = ['나는', '나를', '내가', '너무', '없다', '정말', '것은', '있다.', '자꾸', '싶지', '않다', '같다', '싶다', '했다', '나왔다']

    wordcloud = WordCloud(font_path='moodtracker/static/fonts/AppleSDGothicNeoSB.ttf', background_color='white', stopwords=stopwords, width=800, height=800).generate_from_text(content_text)
    wordcloud.to_file('media/wc_test.png') # 변수로 바꿔야 함
    '''
    plt.figure(figsize=(400,400)) #이미지 사이즈 지정
    plt.imshow(wordcloud)
    plt.axis("off") #x y 축 숫자 제거
    plt.show()
    '''
    wc = Wordcloud() # 워드클라우드 객체 하나 생성
    wc.username = user 
    wc.wc_image = 'wc_test.png' # 변수로 바꿔야 함
    wc.save() # 데이터베이스에 저장


# 작성 내용을 모델에 돌려서 긍정/부정 결과 얻는다.
# !!계속 오류나는 중.
def use_model(content):
    import pickle
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from konlpy.tag import Okt

    #주어진 데이터를 단어 사전으로 만들고 각 단어의 빈도수를 계산한 후 벡터화하는 객체 생성
    tfidf = TfidfVectorizer(lowercase=False, tokenizer=tokenizer)

    # 문장별 나오는 단어 수 세서 수치화, 벡터화해서 학습 시킨다.
    logistic = LogisticRegression(C=10.0, penalty='l2', random_state=0)

    pipe=Pipeline([('vect', tfidf), ('clf', logistic)])

    with open('./static/pipe.dat', 'rb') as fp:
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
    content = request.GET['content']

    mood_record = MoodTracker()
    mood_record.content = content
    # mood_record.mood = request.GET['mood'] 
    mood_record.pub_date = timezone.datetime.now()
    pos_neg = use_model(content)
    mood_record.pos_neg = pos_neg    

    mood_record.save()
    return redirect('/moodtracker/record') # '/moodtracker/' + +str(mood_record.id)


# moodtracker_record.html에서 이전 일기를 보여주거나, 작성 화면 보여준다.
#def show(request):
    # 오늘 날짜이고, 오늘 날짜에 작성된 일기가 없으면
    # write
    # 캘린더에서 오늘 날짜 하이라이트

    # 오늘 혹은 이전 날짜이고, 작성된 일기가 있으면
    # 작성된 일기를 보여준다.
    # 캘린더에서 해당 날짜 하이라이트

    # 이전 날짜이고, 작성된 일기가 없으면
    # 작성하지 않았다는 안내 텍스트
    # 캘린더에서 해당 날짜 하이라이트
    # 팝업

    # 미래의 날짜이면
    # 선택 불가능하거나 작성할 수 없다는 안내 텍스트
    # 캘린더에서 해당 날짜 하이라이트
    # 팝업

