from rest_framework import serializers
from application.models import Application, Cost_Application
from django.utils import timezone


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

    name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    number = serializers.CharField(max_length=20)
    messenger = serializers.ChoiceField(choices=Application.MESSENGER_CHOICES, required=False, allow_blank=True)
    document = serializers.ListField(child=serializers.FileField(), required=False)
    message = serializers.CharField(max_length=255, required=False, allow_blank=True)
    created_time = serializers.DateTimeField(default=timezone.now, read_only=True)


class Cost_ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost_Application
        fields = '__all__'
