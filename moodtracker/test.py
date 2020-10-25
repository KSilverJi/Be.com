import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle

#평점 전처리 함수
def pos_neg_preprocessing(value):
    if value==0 :
        return '0'
    else :
        return '1'

#형태소로 쪼개는 함수
def tokenizer(text):
    okt = Okt()
    return okt.morphs(text)

# 전처리, 데이터 준비
def step1_data_preprocessing():
    # 수집한 데이터를 읽어온다.
    df = pd.read_csv('data_new.csv')

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
    with open('pipe.dat', 'wb') as fp:
        pickle.dump(pipe, fp)

    print('모델 저장 완료')


# 입력 받아서 모델의 예측 결과 확인
def step3_using_model():
    # 객체를 복원한다.
    with open('pipe.dat', 'rb') as fp:
        pipe = pickle.load(fp)

    import numpy as np

    while True :
        text = input('일기를 작성해주세요 : ')

        if text=='quit':
            break

        str = [text]
        # 예측 정확도
        r1 = np.max(pipe.predict_proba(str)*100)

        # 예측 결과
        r2 = pipe.predict(str)[0]

        if r2 == '1' :
            print('긍정적인 리뷰')
        else :
            print('부정적인 리뷰')

        print('정확도 : %.3f' %r1)

# 학습 함수
def learning():
    text_train, text_test, pos_neg_train, pos_neg_test = step1_data_preprocessing()
    step2_learning(text_train, pos_neg_train, text_test, pos_neg_test)

# 테스트 함수
def using():
    step3_using_model()

# 학습, 테스트 시작!
learning()
using()
