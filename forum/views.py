from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Forum
from .forms import ForumUpdate

def home(request):
    forums = Forum.objects.order_by('-id')
    forum_list = Forum.objects.all().order_by('-id')
    paginator = Paginator(forum_list,3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request,'forumhome.html', {'forums':forums,'posts':posts} )

def detail(request, forum_id):
    forum_detail = get_object_or_404(Forum, pk=forum_id)
    return render(request, 'detail.html', {'forum': forum_detail})

def create(request):
    return render(request, 'create.html')

def postcreate(request):
    forum = Forum()
    forum.title = request.POST['title']
    forum.body = request.POST['body']
    forum.images = request.FILES['images']
    forum.pub_date = timezone.datetime.now()
    forum.save()
    return redirect('/forum/detail/' + str(forum.id))

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
 
        return render(request,'update.html', {'form':form})


def delete(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    forum.delete()
    return redirect('/')

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

    return render(request, 'new.html', {'fulltext': full_text, 'total': len(word_list), 'dictionary': word_dictionary.items()} )

def search(request):
    forums = Forum.objects.all().order_by('-id')

    q = request.POST.get('q', "") 

    if q:
        forums = forums.filter(title__icontains=q)
        return render(request, 'search.html', {'forums' : forums, 'q' : q})
    
    else:
        return render(request, 'search.html')
