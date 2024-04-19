from django.urls import path
from blog.views import *

urlpatterns = [

    path('blog/', blog_preview, name='blog_preview'),
    path('blog/<slug:slug>/', get_blog_content, name='blog_content'),
    path('video-blog/', video_blog_preview, name='video_blog_preview'),
    path('video-blog/<slug:slug>/', get_video_blog_content, name='video_blog_content')

]
