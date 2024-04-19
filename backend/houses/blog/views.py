from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from blog.models import Blog, BlogStages, BlogImages, BlogVideos, Video_Blog_Main


def remove_html_tags(text):
    cleaned_text = BeautifulSoup(text, 'html.parser').get_text()
    return cleaned_text


@api_view(['GET'])
def blog_preview(request):
    blog_posts = Blog.objects.filter(is_published=True)
    clean_data = []

    for post in blog_posts:
        cleaned_short_description = remove_html_tags(post.short_description)
        post_data = {
            'title': post.title,
            'time_reading': post.time_reading,
            'short_description': cleaned_short_description,
            'blog_type': post.variant_of_blog_type.blog_type,
            'slug': post.slug,
            'is_published': post.is_published
        }
        clean_data.append(post_data)

    return Response(clean_data)


@api_view(['GET'])
def get_blog_content(requests, slug):
    try:
        content = get_object_or_404(Blog, slug=slug)
        stage_content = BlogStages.objects.filter(blog_content=content)

        clean_data_content = []
        for s in stage_content:
            cleaned_description = remove_html_tags(s.description)
            points = cleaned_description.split('\n')
            clean_points = [point.replace('\r', '').replace('\xa0', '').strip() for point in points]

            post = {
                'stage': s.stage,
                'description': clean_points,
            }

            images = BlogImages.objects.filter(blog_content=content, number_of_stage=s)

            image_urls = []
            for i in images:
                image_urls.append(i.images.url)

            post['stage_photos'] = image_urls

            clean_data_content.append(post)

        videos = BlogVideos.objects.filter(blog_video=content)

        video_urls = []
        for v in videos:
            video_urls.append(v.video_url)

        videos_dict = {'videos': video_urls}

        content_dict = {'content': clean_data_content, **videos_dict}

        return Response(data=content_dict)

    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=404)


@api_view(['GET'])
def video_blog_preview(requests):
    video_blog_posts = Video_Blog_Main.objects.filter(is_published=True)
    clean_data = []

    for post in video_blog_posts:
        cleaned_video_blog_desc = remove_html_tags(post.short_description)
        post_data = {
            'title': post.title,
            'time_watching': post.time_watching,
            'short_description': cleaned_video_blog_desc,
            'slug': post.slug,
            'is_published': post.is_published,
        }

        clean_data.append(post_data)

    return Response(clean_data)


@api_view(['GET'])
def get_video_blog_content(request, slug):
    blog_content = get_object_or_404(Video_Blog_Main, slug=slug)

    cleaned_description = remove_html_tags(blog_content.description)
    video_content = []

    post = {
        "title": blog_content.title,
        "time_watching": blog_content.time_watching,
        "content_video_url": blog_content.content_video_url,
        "description": cleaned_description
    }
    video_content.append(post)

    return Response(video_content)
