from rest_framework import serializers
from .models import House


class HouseSerializerAPI_BOT(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('title', 'main_image', 'floors', 'project_name', 'price', 'area', 'currency', 'slug')


