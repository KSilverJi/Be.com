from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Forum
from .forms import ForumUpdate
from .models import MyProfile,MyClass
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

@login_required
def forum_home(request):
    user = request.user   
    #print(user)  
    forums = Forum.objects.order_by('-id')
    forum_list = Forum.objects.all().order_by('-id')
    paginator = Paginator(forum_list,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    my = MyProfile.objects.get(username=user)
    myclass=MyClass.objects.filter( hak=my.school_year,ban=my.school_class)
    #print(myclass)

    item = {
        'forums':forums,
        'posts':posts,
        'my':my,
        'myclass':myclass
    }
    return render(request,'forum/forumhome.html', item)

@login_required
def detail(request, forum_id):
    user = request.user # 현재 로그인한 사용자
    forum_detail = get_object_or_404(Forum, pk=forum_id)
    person = MyProfile.objects.get(pk=forum_detail.writer.id) # 보여줄 글의 주인

    if person.username==user : # 내가 쓴 글일 때
        detail = 'my'
    else: # 다른 친구가 쓴 글일 때
        detail = 'friend'

    

    item={
        'detail' : detail,
        'forum' : forum_detail,
    }
    return render(request, 'forum/detail.html', item)

@login_required
def create(request):
    return render(request, 'forum/create.html')

@login_required
def postcreate(request):
    user = request.user    
    my = MyProfile.objects.get(username=user)
    forum = Forum()
    forum.title = request.POST['title']
    forum.body = request.POST['body']
    forum.images = request.FILES['images']
    forum.writer = my
    forum.pub_date = timezone.datetime.now()
    #추가
    myclass=MyClass.objects.get(hak=my.school_year,ban=my.school_class)
    if myclass.class_intimacy < 100:
        myclass.class_intimacy += 1 # 친밀도 1% 증가
        myclass.save()

    forum.save()

    return redirect('/forum/detail/' + str(forum.id))

@login_required
def update(request, forum_id):
    forum = Forum.objects.get(id=forum_id)

    if request.method =='POST':
        form = ForumUpdate(request.POST)
        if form.is_valid():
            forum.title = form.cleaned_data['title']
            forum.body = form.cleaned_data['body']
            forum.pub_date=timezone.now()
            forum.save()
            return redirect('/forum/detail/' + str(forum.id))
    else:
        form = ForumUpdate(instance = forum)
 
        return render(request,'forum/update.html', {'form':form})

@login_required
def delete(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    forum.delete()
    return redirect('/')

@login_required
def new(request):
    full_text = request.GET['fulltext']

    word_list = full_text.split()

    word_dictionary = {}

    for word in word_list:
        if word in word_dictionary:
            # Increase
            word_dictionary[word] += 1
        else:
            # add to the dictionary
            word_dictionary[word] = 1

    return render(request, 'forum/new.html', {'fulltext': full_text, 'total': len(word_list), 'dictionary': word_dictionary.items()} )

@login_required
def search(request):
    forums = Forum.objects.all().order_by('-id')

    q = request.POST.get('q', "") 

    if q:
        forums = forums.filter(title__icontains=q)
        return render(request, 'forum/search.html', {'forums' : forums, 'q' : q})
    
    else:
        return render(request, 'forum/search.html')
