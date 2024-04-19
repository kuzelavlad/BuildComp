from django.urls import path
from contacts.views import get_contacts, ContactsAndAddress, SocialNetworksAPI


urlpatterns = [

    path('contacts/', get_contacts, name='contacts'),
    path('api/contacts-and-address/', ContactsAndAddress.as_view(), name='contacts-and-address'),
    path('api/links/', SocialNetworksAPI.as_view(), name='social-networks-api')

]
