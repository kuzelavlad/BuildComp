from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from contacts.models import CountryContacts, Contacts, Address, SocialNetworks
from contacts.serializers import ContactsSerializer, AddressSerializer, SocialNetworksSerializer


@api_view(['GET'])
def get_contacts(request):
    clean_data = []

    countries = CountryContacts.objects.all()

    for country in countries:
        contacts = Contacts.objects.filter(country=country.id)
        address = Address.objects.filter(country=country.id)

        clean_contacts = []

        for contact in contacts:
            contact_data = {
                'title': contact.department,
                'content': contact.phone_number,
                'name': contact.name
            }
            clean_contacts.append(contact_data)

        for addr in address:
            address_data = {
                'title': addr.title_address,
                'content': addr.office_address,
            }
            clean_contacts.append(address_data)

        country_data = {
            'country': country.country,
            'contacts': clean_contacts
        }

        clean_data.append(country_data)

    return Response(clean_data)


class ContactsAndAddress(APIView):
    def get(self, request):
        contacts = Contacts.objects.all()
        address = Address.objects.all()

        contacts_data = ContactsSerializer(contacts, many=True).data
        address_data = AddressSerializer(address, many=True).data

        combined_data = {
            "contacts": contacts_data,
            "address": address_data,
        }

        return Response(combined_data)


class SocialNetworksAPI(APIView):
    def get(self, request):
        social_networks = SocialNetworks.objects.all()
        serializer = SocialNetworksSerializer(social_networks, many=True)
        data = serializer.data
        return Response(data)
