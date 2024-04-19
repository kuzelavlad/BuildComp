from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import time
import re


class Application(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=30, null=True, blank=True)
    number = models.CharField(verbose_name="Номер телефона", max_length=20)
    MESSENGER_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('viber', 'Viber'),
    ]
    messenger = models.CharField(verbose_name="Мессенджер", max_length=10, choices=MESSENGER_CHOICES, null=True,
                                 blank=True)
    message = models.CharField(verbose_name="Сообщения", max_length=255, null=True, blank=True)
    application_number = models.CharField(verbose_name="Номер заявки", max_length=20,
                                          unique=True, null=True, blank=True)
    created_time = models.DateTimeField(verbose_name='Время создания', default=timezone.now)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return f"Заявка #{self.id}"

    class Meta:
        verbose_name = "Заявка Для Обратной Связи"
        verbose_name_plural = "Заявки Для Обратной Связи"


@receiver(post_save, sender=Application)
def set_application_number(sender, instance, created, **kwargs):
    if created and not instance.application_number:
        unique_number = f"{instance.id}-{int(time.time())}"
        instance.application_number = unique_number
        instance.save()


@receiver(pre_save, sender=Application)
def validate_phone_number(sender, instance, **kwargs):
    if not re.match(r'^[0-9+\-()]*$', instance.number):
        raise ValidationError("Поле 'number' должно содержать только цифры, '+', '-', '(', ')' символы")


@receiver(pre_save, sender=Application)
def validate_fields(sender, instance, **kwargs):
    fields_to_validate = ['name']

    for field_name in fields_to_validate:
        field_value = getattr(instance, field_name)
        if field_value is not None and re.search(r'\d', field_value):
            raise ValidationError(f"Поле '{field_name}' не должно содержать цифры.")


class ApplicationFile(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    file = models.FileField(upload_to="documents/")

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = "Прикрепленный файл"
        verbose_name_plural = "Прикрепленные файлы"


class Cost_Application(models.Model):
    SERVICES_CHOICES = (

        ("house", "Строительство Дома"),
        ("sauna", "Строительство Бани"),
        ("gazebo", "Строительство Беседки"),

    )

    PAYMENT_TYPES_CHOICES = (

        ("cash", "Своими Деньгами"),
        ("credit", "Кредит/Рассрочка"),
        ("decree", "240 Указ")

    )

    TYPES_OF_CONSTRUCTION_CHOICES = (

        ("comlex_house", "Домокомплект"),
        ("rough_finish", "Коробка Дома"),
        ("key_house", "Дом Под Ключ"),

    )

    TYPES_OF_ACCOMMODATION_CHOICES = (

        ("permanent_residence", "Для Постоянного Проживания"),
        ("temporary_residence", "Для Временного Проживания")

    )

    name = models.CharField(verbose_name="Имя", max_length=100)
    number = models.CharField(verbose_name="Номер телефона", max_length=30)
    types_of_service = models.CharField(verbose_name="Вид Услуги", choices=SERVICES_CHOICES, max_length=50)
    types_of_payment = models.CharField(verbose_name="Вид Оплаты", choices=PAYMENT_TYPES_CHOICES, max_length=50)
    area = models.PositiveSmallIntegerField(verbose_name="Общая Площадь м2")
    floors = models.PositiveSmallIntegerField(verbose_name="Количество Этажей")
    checkbox_attic = models.BooleanField(verbose_name="Последний Этаж Мансардный", default=False)
    checkbox_ground_floor = models.BooleanField(verbose_name="Наличие Цокольного Этажа", default=False)
    types_of_construction = models.CharField(verbose_name="Вид Строительства", choices=TYPES_OF_CONSTRUCTION_CHOICES,
                                             max_length=50, null=True, blank=True)
    types_of_accommodation = models.CharField(verbose_name="Вариант Проживания", max_length=20)
    number_of_residents = models.PositiveSmallIntegerField(verbose_name="Количество Проживающих")
    checkbox_canalization = models.BooleanField(verbose_name="Наличие Канализации", default=False)
    checkbox_borehole = models.BooleanField(verbose_name="Наличие Скважины", default=False)
    country = models.CharField(verbose_name="Страна", max_length=100)
    district = models.CharField(verbose_name="Район", max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name="Город", max_length=100)
    cost_application_number = models.CharField(verbose_name="Номер заявки", max_length=20,
                                               unique=True, null=True, blank=True)
    created_time = models.DateTimeField(verbose_name='Время создания', default=timezone.now)

    def __str__(self):
        if self.cost_application_number:
            return f"Заявка №{self.cost_application_number}"

    class Meta:
        verbose_name = "Заявка На Строительство"
        verbose_name_plural = "Заявки На Строительство"


@receiver(post_save, sender=Cost_Application)
def set_cost_application_number(sender, instance, created, **kwargs):
    if created and not instance.cost_application_number:
        unique_number = f"{instance.id}-{int(time.time())}"
        instance.cost_application_number = unique_number
        instance.save()


@receiver(pre_save, sender=Cost_Application)
def validate_number(sender, instance, **kwargs):
    if not re.match(r'^[0-9+\-()]*$', instance.number):
        raise ValidationError("Поле 'number' должно содержать только цифры, '+', '-', '(', ')' символы")


@receiver(pre_save, sender=Cost_Application)
def validate_field(sender, instance, **kwargs):
    field_to_validate = ['name']

    for field_name in field_to_validate:
        field_value = getattr(instance, field_name)
        if field_value is not None and re.search(r'\d', field_value):
            raise ValidationError(f"Поле '{field_name}' не должно содержать цифры.")
