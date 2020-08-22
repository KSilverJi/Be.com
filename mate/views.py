from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse("<h1>이 곳은 mate의 페이지입니다</h1>")
    return render(request, 'mate/mate.html')

