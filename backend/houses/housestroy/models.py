from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class BaseDateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Styles(models.Model):
    title = models.CharField(verbose_name="Название Стиля", max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Cтиль"
        verbose_name_plural = "Стили"


class SortHouse(models.Model):
    title = models.CharField(verbose_name="Наименование", max_length=255, unique=True)

    def __str__(self) -> CharField:
        return self.title

    class Meta:
        verbose_name = "Вид Дома"
        verbose_name_plural = "Виды Домов"


class House(models.Model):
    CURRENCY_CHOICES = (
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("BYN", "BYN"),
        ("RUB", "RUB"),

    )
    title = models.CharField(verbose_name="Название дома", max_length=255, unique=True)
    sort_of_house = models.ForeignKey(
        SortHouse,
        on_delete=models.CASCADE,
        verbose_name="Вид Дома"
    )
    project_name = models.CharField(verbose_name="Номер проекта", max_length=50, unique=True)
    main_image = models.ImageField(verbose_name="Заглавное Фото", upload_to="photos/", max_length=50)
    floors = models.PositiveIntegerField(verbose_name="Количество Этажей")
    rooms = models.PositiveIntegerField(verbose_name="Количество Комнат")
    bathrooms = models.PositiveIntegerField(verbose_name="Количество Санузлов")
    house_style = models.ForeignKey(
        Styles,
        verbose_name="Стиль",
        max_length=50,
        on_delete=models.SET_NULL,
        null=True
    )
    area = models.FloatField(verbose_name="Площадь м2")
    price = models.DecimalField(verbose_name="Стоимость", max_digits=15, decimal_places=2)
    currency = models.CharField(verbose_name="Валюта", choices=CURRENCY_CHOICES, max_length=20)
    full_description = models.TextField(verbose_name='Полное описание', max_length=255)
    slug = models.SlugField(unique=True, db_index=True)
    video_url = models.TextField(verbose_name="Cсылка на видео", null=True, blank=True)
    created_time = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name='Время модификации', auto_now=True)
    is_published = models.BooleanField(verbose_name="Опубликовано", default=False)

    def __str__(self) -> str:
        return f"{self.title} | {self.project_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_name)
        super(House, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # return reverse('get_house', kwargs={'slug': self.slug})
        return reverse('get_house', args=[str(self.slug)])

    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"


class Image(models.Model):
    image = models.ImageField(verbose_name="Изображение", upload_to="photos/")
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        verbose_name="Дом",
    )

    def clean(self):
        # Проверяем, есть ли уже другие изображения с таким же именем внутри этого дома
        if Image.objects.filter(house=self.house, image=self.image).exclude(pk=self.pk).exists():
            raise ValidationError('Фотография с таким именем уже существует внутри этого дома.')

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем проверку при сохранении
        super(Image, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Фото "
        verbose_name_plural = "Фото"


class Schema(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=255, null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    image = models.ImageField(verbose_name="Изображение", upload_to="schema_photos/")
    floor = models.PositiveIntegerField(verbose_name="Номер Этажа")
    floor_point = models.TextField(verbose_name="Пункты Этажа")
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        verbose_name="Дом",
        related_name='schemes'
    )

    def __str__(self) -> str:
        return f"Дом: {self.house} | Этаж: {self.floor}"

    class Meta:
        verbose_name = "Планировка"
        verbose_name_plural = "Планировка"


class HousePoints(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        verbose_name="Дом"

    )
    point = models.CharField(verbose_name="Пункт", max_length=255)

    class Meta:
        verbose_name = "Пункт Описания Работ"
        verbose_name_plural = "Пункт Описания Работ"


class Overhead_View(models.Model):
    house = models.ForeignKey(
        House,
        verbose_name="Дом",
        on_delete=models.CASCADE
    )
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    title_description = RichTextField(verbose_name='Описание')
    plan_title = models.CharField(verbose_name='Заголовок Планировки', max_length=100)
    plan_title_description = RichTextField(verbose_name='Описание')
    overhead_image = models.ImageField(verbose_name='Изображение', upload_to='overhead_photos/')

    class Meta:
        verbose_name = "Фото Вида Сверху"
        verbose_name_plural = "Фото Вида Сверху"


class Equipment_Types(models.Model):
    equipment_type = models.CharField(verbose_name='Вид Комплектации', max_length=55)

    def __str__(self):
        return self.equipment_type

    class Meta:
        verbose_name = "Вид Комплектации"
        verbose_name_plural = "Виды Комплектации"


class Equipment_Options(models.Model):
    CURRENCY_CHOICES = (

        ("USD", "USD"),
        ("EUR", "EUR"),
        ("BYN", "BYN"),
        ("RUB", "RUB"),

    )
    house = models.ForeignKey(

        House,
        on_delete=models.CASCADE,
        verbose_name="Дом"

    )
    variant_of_equipment_type = models.ForeignKey(
        Equipment_Types,
        on_delete=models.CASCADE,
        verbose_name="Вид Комплектации"
    )
    point = models.CharField(verbose_name="Пункт Работ", max_length=255)
    point_description = models.TextField(verbose_name="Описание Пункта")
    currency = models.CharField(verbose_name="Валюта", choices=CURRENCY_CHOICES, max_length=20)
    point_price = models.PositiveIntegerField(verbose_name="Стоимость")

    def __str__(self):
        return f"{self.point} - {self.variant_of_equipment_type}"

    class Meta:
        verbose_name = "Вариант Комплектации"
        verbose_name_plural = "Варианты Комплектации"


class Equipment_Button(models.Model):
    house = models.ForeignKey(
        House,
        verbose_name="Дом",
        on_delete=models.CASCADE
    )
    button = models.CharField(verbose_name='Название Кнопки', max_length=20)
    button_url = models.TextField(verbose_name='Ссылка Кнопки')

    def __str__(self):
        return self.button

    class Meta:
        verbose_name = "Кнопка"
        verbose_name_plural = "Кнопки"


class InteriorImage(models.Model):
    image = models.ImageField(verbose_name="Изображение", upload_to="interior_photos/")
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        verbose_name="Дом",
    )

    class Meta:
        verbose_name = "Фото Интерьера"
        verbose_name_plural = "Фото Интерьера"


class Construction_Description(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        verbose_name="Дом"
    )
    title = models.CharField(verbose_name='Заголовок', max_length=100, default="Введите заголовок")
    description = RichTextField(verbose_name='Описание')

    class Meta:
        verbose_name = "Описание Процесса Строительства"
        verbose_name_plural = "Описание Процесса Строительства"


class Construction_Image(models.Model):
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
        verbose_name="Дом"
    )
    image = models.ImageField(verbose_name='Изображение', upload_to="construction_photos/")

    class Meta:
        verbose_name = "Фото Строительства Дома"
        verbose_name_plural = "Фото Строительства Дома"
