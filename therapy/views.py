from django.shortcuts import render, redirect
from .models import Counsel

import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def therapy(request):
    return render(request, 'counsel.html')

@login_required
def result(request):
    today = datetime.datetime.today()

    if request.method == "POST":
        counsel=Counsel()
        counsel.username = User.objects.get(username=request.user.username)

        counsel.who = request.POST.get('who')
        counsel.how = request.POST.get('how')
        counsel.teacher = request.POST.get('teacher').rstrip(' 선생님')
        counsel.detailtext = request.POST.get('detailtext', '')
        counsel.about = request.POST.getlist('about[]')

        counsel.datenum = str(today.year) + '년' + str(today.month) + '월' + request.POST.get('datenum') + '일'

        counsel.timepick = request.POST.getlist('time-pick[]')
        counsel.save()
    return render(request, 'result.html')