# Generated by Django 4.2.5 on 2023-11-15 19:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Имя')),
                ('number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('messenger', models.CharField(blank=True, choices=[('whatsapp', 'WhatsApp'), ('telegram', 'Telegram'), ('viber', 'Viber')], max_length=10, null=True, verbose_name='Мессенджер')),
                ('message', models.CharField(blank=True, max_length=255, null=True, verbose_name='Сообщения')),
                ('application_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Номер заявки')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Заявка Для Обратной Связи',
                'verbose_name_plural': 'Заявки Для Обратной Связи',
            },
        ),
        migrations.CreateModel(
            name='Cost_Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('number', models.CharField(max_length=30, verbose_name='Номер телефона')),
                ('types_of_service', models.CharField(choices=[('house', 'Строительство Дома'), ('sauna', 'Строительство Бани'), ('gazebo', 'Строительство Беседки')], max_length=50, verbose_name='Вид Услуги')),
                ('types_of_payment', models.CharField(choices=[('cash', 'Своими Деньгами'), ('credit', 'Кредит/Рассрочка'), ('decree', '240 Указ')], max_length=50, verbose_name='Вид Оплаты')),
                ('area', models.PositiveSmallIntegerField(verbose_name='Общая Площадь м2')),
                ('floors', models.PositiveSmallIntegerField(verbose_name='Количество Этажей')),
                ('checkbox_attic', models.BooleanField(default=False, verbose_name='Последний Этаж Мансардный')),
                ('checkbox_ground_floor', models.BooleanField(default=False, verbose_name='Наличие Цокольного Этажа')),
                ('types_of_construction', models.CharField(blank=True, choices=[('comlex_house', 'Домокомплект'), ('rough_finish', 'Коробка Дома'), ('key_house', 'Дом Под Ключ')], max_length=50, null=True, verbose_name='Вид Строительства')),
                ('types_of_accommodation', models.CharField(max_length=20, verbose_name='Вариант Проживания')),
                ('number_of_residents', models.PositiveSmallIntegerField(verbose_name='Количество Проживающих')),
                ('checkbox_canalization', models.BooleanField(default=False, verbose_name='Наличие Канализации')),
                ('checkbox_borehole', models.BooleanField(default=False, verbose_name='Наличие Скважины')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('district', models.CharField(blank=True, max_length=100, null=True, verbose_name='Район')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('cost_application_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Номер заявки')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Заявка На Строительство',
                'verbose_name_plural': 'Заявки На Строительство',
            },
        ),
        migrations.CreateModel(
            name='ApplicationFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.application')),
            ],
            options={
                'verbose_name': 'Прикрепленный файл',
                'verbose_name_plural': 'Прикрепленные файлы',
            },
        ),
    ]
