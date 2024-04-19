from django.contrib import admin
from blog.models import Blog, BlogStages, BlogImages, BlogVideos, Video_Blog_Main, Blog_Type


class BlogStageInline(admin.TabularInline):
    model = BlogStages
    extra = 0


class BlogImageInline(admin.TabularInline):
    model = BlogImages
    extra = 0


class BlogVideosInline(admin.TabularInline):
    model = BlogVideos
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "variant_of_blog_type",
        "is_published"

    ]
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogStageInline, BlogImageInline, BlogVideosInline]
    list_editable = ['is_published']


@admin.register(Video_Blog_Main)
class VideoBlogMainAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "time_watching",
        "is_published"
    ]
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']


@admin.register(Blog_Type)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ["blog_type"]
