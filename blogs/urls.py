from django.urls import path
from . import views

urlpatterns =[
   path('', views.hello, name='hello'), 
   path('home', views.home, name='home'), 
   path('about', views.about, name='about'), 
   path('contact', views.contact, name='contact'), 
   path('blogs', views.blogs, name='blogs'),
   path('blog/<slug:slug>', views.blog_detail, name='blog_detail'), 
   path('blogs/<int:post_id>', views.blog_detail, name='blog_detail'), 
   
]