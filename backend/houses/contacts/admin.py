from django.contrib import admin
from contacts.models import Contacts, Address, CountryContacts, SocialNetworks


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ["department", "phone_number", "name", "country"]
    list_filter = ["department", "country"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["country", "office_address"]


@admin.register(CountryContacts)
class CountryContactsAdmin(admin.ModelAdmin):
    list_display = ["country"]


@admin.register(SocialNetworks)
class SocialNetworksAdmin(admin.ModelAdmin):
    list_display = [
        "title_messanger",
        "link_messanger"
    ]
