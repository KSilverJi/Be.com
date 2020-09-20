from django.shortcuts import render, redirect
from .models import Counsel

# Create your views here.
def therapy(request):
    return render(request, 'counsel.html')


def result(request):
    if request.method == "POST":
        counsel=Counsel()
        counsel.who = request.POST.get('who')
        counsel.how = request.POST.get('how')
        counsel.teacher = request.POST.get('teacher')
        counsel.detailtext = request.POST.get('detailtext', '')
        counsel.about = request.POST.getlist('about[]')
        counsel.datenum = request.POST.get('datenum')
        counsel.timepick = request.POST.getlist('time-pick[]')
        counsel.save()
    return render(request, 'result.html')