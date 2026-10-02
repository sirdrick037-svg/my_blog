from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

# Create your views here.
def hello(request):
    return HttpResponse('Hello World!')

def home(request):
    context = {
        'sentence': 'She went to the bank',
        'name': 'sarah',
        'age': 30,
        'place': 'Nairobi',
        'reason': 'to deposit some cash',
    }
    return render(request, 'index.html', context)


def about(request):
    data = {
        "reason": "This website was created to share information and ideas."
    }

    return render(request, "about.html", data)


def contact(request):
    return render(request, "contact.html")

def blogs(request):
    posts = Post.objects.all()
    return render(request, 'blogs.html', {"posts":posts})

def blog_detail(request, slug):
    #post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog_detail.html", {"post":post})

# try:
#     post = Post.objects.get(id=post_id)
# except Post.DoesNotExixt:
#     raise Http404    
