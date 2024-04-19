from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from housestroy.models import House


class BaseDateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog_Type(models.Model):
    blog_type = models.CharField(verbose_name='Категория', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.blog_type

    class Meta:
        verbose_name = "Категория Статьи"
        verbose_name_plural = "Категории Статей"


class Blog(models.Model):
    title = models.CharField(verbose_name="Название Статьи", max_length=255, unique=True)
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        verbose_name="Дом",
        null=True,
        blank=True
    )
    variant_of_blog_type = models.ForeignKey(
        Blog_Type,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        null=True,
        blank=True

    )
    time_reading = models.PositiveIntegerField(verbose_name="Время Прочтения Статьи (мин)")
    short_description = RichTextField(verbose_name="Краткое Описание")
    slug = models.SlugField(unique=True, db_index=True)
    created_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='Время модификации', auto_now=True)
    is_published = models.BooleanField(verbose_name="Опубликовано", default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # return reverse('get_blog_content', kwargs={'slug': self.slug})
        return reverse('get_blog_content', args=[str(self.slug)])

    class Meta:
        verbose_name = "Cтатья"
        verbose_name_plural = "Статьи"


class BlogStages(models.Model):
    stage = models.CharField(verbose_name="Этап", max_length=100)
    description = RichTextField(verbose_name="Описание")
    blog_content = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name="Статья"
    )

    def __str__(self):
        return self.stage

    class Meta:
        verbose_name = "Этап"
        verbose_name_plural = "Этапы"


class BlogImages(models.Model):
    images = models.ImageField(verbose_name="", upload_to="blog_photos/")
    blog_content = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name="Cтатья"
    )
    number_of_stage = models.ForeignKey(
        BlogStages,
        on_delete=models.CASCADE,
        verbose_name="Этап"

    )

    class Meta:
        verbose_name = "Фото Этапа"
        verbose_name_plural = "Фото Этапов"


class BlogVideos(models.Model):
    video_url = models.TextField(verbose_name="Ссылка на Видео")
    blog_video = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"


class Video_Blog_Main(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    time_watching = models.PositiveIntegerField(verbose_name='Длительность (мин.)')
    short_description = RichTextField(verbose_name='Краткое Описание')
    main_video_url = models.TextField(verbose_name='Ссылка на Главное Видео')
    description = RichTextField(verbose_name="Содержание Статьи")
    content_video_url = models.TextField(verbose_name='Ссылка на Видео')
    slug = models.SlugField(unique=True, db_index=True)
    created_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='Время модификации', auto_now=True)
    is_published = models.BooleanField(verbose_name="Опубликовано", default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Video_Blog_Main, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     # return reverse('get_house', kwargs={'slug': self.slug})
    #     return reverse('get_house', args=[str(self.slug)])

    class Meta:
        verbose_name = "Видео-Блог"
        verbose_name_plural = "Видео-Блог"
