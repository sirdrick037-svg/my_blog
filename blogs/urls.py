from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello, name='hello'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blogs/create/', views.create_post, name='create_post'),
    path('blogs/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('accounts/', include('django.contrib.auth.urls')),
]