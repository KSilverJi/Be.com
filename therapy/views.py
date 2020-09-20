from django.shortcuts import render, redirect
from .models import Counsel

import datetime

# Create your views here.
def therapy(request):
    return render(request, 'counsel.html')


def result(request):

    today = datetime.datetime.today()

    if request.method == "POST":
        counsel=Counsel()
        counsel.who = request.POST.get('who')
        counsel.how = request.POST.get('how')
        counsel.teacher = request.POST.get('teacher')
        counsel.detailtext = request.POST.get('detailtext', '')
        counsel.about = request.POST.getlist('about[]')

        counsel.datenum = str(today.year) + '년' + str(today.month) + '월' + request.POST.get('datenum') + '일'

        counsel.timepick = request.POST.getlist('time-pick[]')
        counsel.save()
    return render(request, 'result.html')