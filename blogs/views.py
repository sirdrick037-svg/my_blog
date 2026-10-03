from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Post
from .forms import PostForm

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

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Assign the currently logged-in user.
            post.user = request.user
            post.save()
            return redirect("blog_detail", slug=post.slug)
    else:
        form = PostForm()

    return render(
        request,
        "post_form.html",
        {
            "form": form,
            "page_title": "Create Post",
            "button_text": "Publish Post",
        },
    )

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only the author can edit the post.
    if post.user != request.user:
        return redirect("blog_detail", slug=post.slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "post_form.html",
        {
            "form": form,
            "page_title": "Edit Post",
            "button_text": "Update Post",
            "post": post,
        },
    )

# try:
#     post = Post.objects.get(id=post_id)
# except Post.DoesNotExixt:
#     raise Http404    
