from django.utils import timezone
from rest_framework import serializers
from contacts.models import Contacts, Address


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('department', 'phone_number', 'name')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('title_address', 'office_address')


class SocialNetworksSerializer(serializers.Serializer):
    messengerName = serializers.CharField(source='title_messanger')
    linkToMessenger = serializers.CharField(source='link_messanger')
    image = serializers.ImageField(source='messanger_image')
