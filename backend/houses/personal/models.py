from django.db import models
from ckeditor.fields import RichTextField


class BaseDateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Personal(models.Model):
    name = models.CharField(verbose_name="ФИО", max_length=255)
    department = models.CharField(verbose_name="Отдел", max_length=255, null=True, blank=True)
    position = models.CharField(verbose_name="Должность", max_length=255)
    pers_image = models.ImageField(verbose_name="Фото", upload_to="personal_photos/")
    description = RichTextField(verbose_name="Описание")

    def __str__(self):
        return f'{self.name} | {self.department}'

    class Meta:
        verbose_name = "Персонал"
        verbose_name_plural = "Персонал"
