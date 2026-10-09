from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Author, Post, Subscriber
from .forms import PostForm, SubscribeForm
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings
from django.utils.html import escape

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
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            author, _ = Author.objects.get_or_create(
                email=request.user.email,
                defaults={
                    "first_name": request.user.first_name or request.user.username,
                    "last_name": request.user.last_name,
                },
            )
            post.author = author
            post.save()
            messages.success(request, "Post created successfully.")
            return redirect("blog_detail", slug=post.slug)
    else:
        form = PostForm()
        messages.error(request, "There was a problem saving the post.")

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
    if post.author.email != request.user.email:
        return redirect("blog_detail", slug=post.slug)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
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


@require_http_methods(['GET', 'POST'])
def subscribe(request):
    form = SubscribeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email'].strip().lower()
        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, 'You are already subscribed.')
        else:
            Subscriber.objects.create(email=email)
            try:
                _send_subscriber_welcome_email(email)
            except Exception:
                messages.warning(
                    request,
                    'You are subscribed, but we could not send the confirmation email right now.',
                )
            else:
                messages.success(
                    request,
                    'You are subscribed. A welcome note is on its way to your inbox.',
                )
            return redirect('subscribe')
    return render(request, 'subscribe.html', {'form': form})


def _send_subscriber_welcome_email(email):
    site_name = str(settings.SITE_NAME)
    html_site_name = escape(site_name)
    site_url = str(settings.SITE_URL).rstrip('/')
    subject = f'Welcome to {site_name}'
    text_body = (
        f'Welcome to {site_name}.\n\n'
        'Thank you for subscribing. You will receive occasional stories, '
        'ideas and learning notes from us.\n\n'
        f'Explore the journal: {site_url}/blog/\n\n'
        f'The {site_name} team'
    )
    html_body = f'''<!doctype html>
<html lang="en">
<body style="margin:0;padding:0;background:#f6f4ee;color:#202e27;font-family:Arial,sans-serif;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f6f4ee;padding:36px 12px;">
    <tr><td align="center">
      <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;background:#ffffff;border:1px solid #e3dfd4;">
        <tr><td style="padding:38px 42px 18px;border-bottom:1px solid #e3dfd4;">
          <p style="margin:0;color:#746044;font-size:12px;font-weight:bold;letter-spacing:3px;text-transform:uppercase;">{html_site_name}</p>
        </td></tr>
        <tr><td style="padding:34px 42px 42px;">
          <h1 style="margin:0 0 18px;color:#17241e;font-family:Georgia,serif;font-size:34px;font-weight:normal;line-height:1.15;">A warm welcome.</h1>
          <p style="margin:0 0 16px;color:#46524b;font-size:16px;line-height:1.7;">Thank you for subscribing. You are now on the list.</p>
          <p style="margin:0 0 26px;color:#46524b;font-size:16px;line-height:1.7;">We will send you occasional stories, considered ideas and learning notes—only when we have something worth sharing.</p>
          <a href="{site_url}/blog/" style="display:inline-block;background:#5b4b38;color:#ffffff;padding:13px 20px;text-decoration:none;font-size:14px;font-weight:bold;">Explore the journal</a>
          <p style="margin:34px 0 0;color:#77796f;font-size:14px;line-height:1.6;">With best wishes,<br>The {html_site_name} team</p>
        </td></tr>
      </table>
      <p style="margin:18px 0 0;color:#77796f;font-size:12px;">You received this message because this address was subscribed on {html_site_name}.</p>
    </td></tr>
  </table>
</body>
</html>'''
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)


def error_404_view(request, exception):
    return render(request, '404.html', status=404)


# try:
#     post = Post.objects.get(id=post_id)
# except Post.DoesNotExixt:
#     raise Http404    
