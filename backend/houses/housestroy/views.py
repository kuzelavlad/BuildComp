from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from .serializers import HouseSerializerAPI_BOT
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from .models import House, Image, HousePoints, Schema, \
    InteriorImage, Equipment_Options, Construction_Image, \
    Construction_Description, Overhead_View, Equipment_Button


def remove_html_tags(text):
    cleaned_text = BeautifulSoup(text, 'html.parser').get_text()
    return cleaned_text


@api_view(['GET'])
def home_page(requests):
    houses = House.objects.filter(is_published=True)[:5].prefetch_related(
        'image_set')  # Используем prefetch_related для загрузки изображений
    clean_data = []
    for house in houses:
        house_data = {
            'title': house.title,
            'main_image': house.main_image.url,
            'floors': house.floors,
            'rooms': house.rooms,
            'area': house.area,
            'price': house.price,
            'currency': house.currency,
            'slug': house.slug,
        }

        images = house.image_set.all()[:2]
        photos = [image.image.url for image in images]
        house_data['photos'] = photos

        clean_data.append(house_data)

    return Response(clean_data)


@api_view(['GET'])
def catalog(requests):
    houses = House.objects.filter(is_published=True)
    clean_data = []
    for i in houses:
        house = {
            'title': i.title,
            'area': i.area,
            'price': i.price,
            'currency': i.currency,
            'main_image': i.main_image.url,
            'project_name': i.project_name,
            'floors': i.floors,
            'sort_of_house': i.sort_of_house.title,
            'slug': i.slug,

        }

        clean_data.append(house)

    return Response(clean_data)


@api_view(['GET'])
def get_house(requests, slug):
    house_object = get_object_or_404(House, slug=slug)

    house_points = HousePoints.objects.filter(house=house_object)
    clean_points = [point.point for point in house_points]

    house_images = Image.objects.filter(house=house_object)
    photos = [image.image.url for image in house_images]

    house = {
        'title': house_object.title,
        'full_description': house_object.full_description,
        'project_name': house_object.project_name,
        'main_image': house_object.main_image.url,
        'floors': house_object.floors,
        'rooms': house_object.rooms,
        'bathrooms': house_object.bathrooms,
        'house_style': house_object.house_style.title,
        'area': house_object.area,
        'video_url': house_object.video_url,
        'price': house_object.price,
        'currency': house_object.currency,
        'points': clean_points,
        'photos': photos,
    }

    interior_photos = [im.image.url for im in InteriorImage.objects.filter(house=house_object)]
    house['interior_photos'] = interior_photos

    schema_objects = Schema.objects.filter(house=house_object)
    for schema in schema_objects:
        floor_points = str(schema.floor_point).split('\r')
        clean_points = [point.split('\n')[1] if len(point.split('\n')) > 1 else point for point in floor_points]

        floor_data = {
            'title': schema.title,
            'description': schema.description,
            'image': schema.image.url,
            'floor': schema.floor,
            'points': clean_points
        }

        house[f'floor_{schema.floor}'] = floor_data

    overhead_view_obj = Overhead_View.objects.filter(house=house_object)

    for overhead in overhead_view_obj:
        clean_title_description, clean_plan_title_description = remove_html_tags(
            overhead.title_description), remove_html_tags(overhead.plan_title_description)
        overhead_data = {
            'title': overhead.title,
            'title_description': clean_title_description,
            'plan_title': overhead.plan_title,
            'plan_title_description': clean_plan_title_description,
            'overhead_image': overhead.overhead_image.url,

        }
        house['overhead_info'] = overhead_data

    equipment_options = Equipment_Options.objects.filter(house=house_object)
    equipment_buttons = Equipment_Button.objects.filter(house=house_object)

    equipment_options_dict = {}
    equipment_buttons_list = []

    for option in equipment_options:
        type_name = option.variant_of_equipment_type.equipment_type
        if type_name not in equipment_options_dict:
            equipment_options_dict[type_name] = []

        equipment_options_dict[type_name].append({
            'point': option.point,
            'point_description': option.point_description,
            'currency': option.currency,
            'price': option.point_price,
        })

    for button in equipment_buttons:
        equipment_buttons_list.append({
            'button': button.button,
            'button_url': button.button_url,
        })

    # Convert the dictionaries to a list of dictionaries for consistent formatting
    equipment_options_list = [{'equipment_type': key, 'content': value} for key, value in
                              equipment_options_dict.items()]

    house['equipment_options'] = equipment_options_list
    house['equipment_buttons'] = equipment_buttons_list

    const_desc = {}
    const_description_info = Construction_Description.objects.filter(house=house_object)
    for const in const_description_info:
        cleaned_description = remove_html_tags(const.description)
        const_desc = {
            'title': const.title,
            'description': cleaned_description
        }
    house['construction_description'] = const_desc

    const_photos = [im.image.url for im in Construction_Image.objects.filter(house=house_object)]
    house['construction_photos'] = const_photos

    return Response(house)


class HouseListView(generics.ListAPIView):
    queryset = House.objects.filter(is_published=True)
    serializer_class = HouseSerializerAPI_BOT
