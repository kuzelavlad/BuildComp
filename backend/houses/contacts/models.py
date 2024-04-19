from django.db import models


class BaseDateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CountryContacts(models.Model):
    country = models.CharField(verbose_name="Страна", max_length=100)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class Contacts(models.Model):
    country = models.ForeignKey(
        CountryContacts,
        on_delete=models.CASCADE,
        verbose_name="Местонахождение Офиса",
    )
    department = models.CharField(verbose_name="Название отдела", max_length=255)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=50)
    name = models.CharField(verbose_name="Имя", max_length=100)

    def __str__(self):
        return f'{self.name} | {self.department}'

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class Address(models.Model):
    title_address = models.CharField(verbose_name='Название Офиса', max_length=255, )
    country = models.ForeignKey(
        CountryContacts,
        on_delete=models.CASCADE,
        verbose_name="Местонахождение Офиса",
    )
    office_address = models.CharField(verbose_name="Адрес", max_length=255)

    def __str__(self):
        return self.title_address

    class Meta:
        verbose_name = "Адреса"
        verbose_name_plural = "Адреса"


class SocialNetworks(models.Model):

    title_messanger = models.CharField(verbose_name='Название Социальной Сети', max_length=100)
    link_messanger = models.TextField(verbose_name='Ссылка')
    messanger_image = models.ImageField(verbose_name='Фото')

    def __str__(self):
        return self.title_messanger

    class Meta:
        verbose_name = "Социальная Cеть"
        verbose_name_plural = "Социальные Cети"


