from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import House


class HomePageViewTest(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.house1 = House.objects.create(
            title="House 1",
            main_image="path/to/main_image1.jpg",
            floors=2,
            rooms=3,
            area=150,
            price=100000,
            currency="USD",
            slug="house-1",
            is_published=True
        )

        # Создаем клиент API
        self.client = APIClient()

    def test_home_page_view(self):
        url = reverse('home_page')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что в ответе есть ожидаемые поля
        self.assertIn('clean_data', response.data)
        self.assertTrue(len(response.data['clean_data']) > 0)


class CatalogViewTest(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.house1 = House.objects.create(
            title="House 1",
            area=150,
            price=100000,
            currency="USD",
            main_image="path/to/main_image1.jpg",
            project_name="Project 1",
            floors=2,
            slug="house-1",
            is_published=True
        )

        # Создаем клиент API
        self.client = APIClient()

    def test_catalog_view(self):
        url = reverse('catalog')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что ответ содержит ожидаемые поля
        self.assertIn('clean_data', response.data)
        self.assertTrue(len(response.data['clean_data']) > 0)

        # Проверяем, что каждый элемент в списке имеет необходимые поля
        for house_data in response.data['clean_data']:
            self.assertIn('title', house_data)
            self.assertIn('area', house_data)
            self.assertIn('price', house_data)
            self.assertIn('currency', house_data)
            self.assertIn('main_image', house_data)
            self.assertIn('project_name', house_data)
            self.assertIn('floors', house_data)
            self.assertIn('slug', house_data)


class GetHouseViewTest(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.house1 = House.objects.create(
            title="House 1",
            full_description="Description 1",
            project_name="Project 1",
            main_image="path/to/main_image1.jpg",
            floors=2,
            rooms=3,
            bathrooms=2,
            house_style="Style 1",
            area=150,
            video_url="https://www.example.com/video",
            price=100000,
            currency="USD",
            slug="house-1",
        )

        # Создаем клиент API
        self.client = APIClient()

    def test_get_house_view(self):
        slug = 'house-1'  # Замените на актуальный slug вашего тестового дома
        url = reverse('get_house', kwargs={'slug': slug})  # Замените 'get_house' на имя вашего URL-пути

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что ответ содержит ожидаемые поля
        self.assertIn('house', response.data)
        house_data = response.data['house']
        self.assertIn('title', house_data)
        self.assertIn('full_description', house_data)
        self.assertIn('project_name', house_data)
        self.assertIn('main_image', house_data)
        self.assertIn('floors', house_data)
        self.assertIn('rooms', house_data)
        self.assertIn('bathrooms', house_data)
        self.assertIn('house_style', house_data)
        self.assertIn('area', house_data)
        self.assertIn('video_url', house_data)
        self.assertIn('price', house_data)
        self.assertIn('currency', house_data)
        self.assertIn('points', house_data)
        self.assertIn('photos', house_data)
        self.assertIn('interior_photos', house_data)


    def test_get_contacts_view(self):
        url = reverse('get_contacts')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что ответ содержит ожидаемые данные
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) > 0)

        # Проверяем структуру данных в ответе
        for country_data in response.data:
            self.assertIsInstance(country_data, dict)
            self.assertIn('country', country_data)
            self.assertIn(country_data['country'], ['Country 1'])  # Замените на реальные значения стран

            self.assertIn('contacts', country_data)
            contacts_data = country_data['contacts']
            self.assertIsInstance(contacts_data, list)
            self.assertTrue(len(contacts_data) > 0)

            for contact_data in contacts_data:
                self.assertIsInstance(contact_data, dict)
                self.assertIn('title', contact_data)
                self.assertIn('content', contact_data)
                self.assertIn('name', contact_data)
