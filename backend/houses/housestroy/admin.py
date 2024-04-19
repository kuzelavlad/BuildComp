from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import House, Image, Styles, Schema, SortHouse, \
    HousePoints, InteriorImage, Equipment_Options, Construction_Image, \
    Construction_Description, Equipment_Types, Overhead_View, Equipment_Button

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Group)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class HousePointsInline(admin.TabularInline):
    model = HousePoints
    extra = 0


class SchemaInline(admin.StackedInline):
    model = Schema
    show_change_link = True
    extra = 0


class InteriorImageInline(admin.TabularInline):
    model = InteriorImage
    extra = 0


class EquipmentOptionsInline(admin.TabularInline):
    model = Equipment_Options
    extra = 1


class ConstructionImageInline(admin.TabularInline):
    model = Construction_Image
    extra = 1


class ConstructionDescriptionInline(admin.TabularInline):
    model = Construction_Description
    extra = 1


class OverheadViewInline(admin.TabularInline):
    model = Overhead_View
    extra = 1


class EquipmentButtonInline(admin.TabularInline):
    model = Equipment_Button
    extra = 1


#   TODO:
#    доработать поля, которые должны переноситься в новый объект после копирования.


# функиция создания копии для объекта Дома
def copy_selected_houses(modeladmin, request, queryset):
    for house in queryset:

        new_house = House()

        # Копируйте только необходимые поля из старого дома в новый
        new_house.title = f"Копия {house.title}"
        new_house.sort_of_house = house.sort_of_house
        new_house.project_name = f"Копия {house.project_name}"
        new_house.main_image = house.main_image
        new_house.floors = house.floors
        new_house.rooms = house.rooms
        new_house.bathrooms = house.bathrooms
        new_house.house_style = house.house_style
        new_house.area = house.area
        new_house.price = house.price
        new_house.currency = house.currency
        new_house.full_description = house.full_description

        # Проверка на уникальность project_name
        while House.objects.filter(project_name=new_house.project_name).exists():
            new_house.project_name = f"Копия {new_house.project_name}"

        new_house.save()


copy_selected_houses.short_description = "Копировать выбранные дома"


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "project_name",
        "house_style",
        "price",
        'area',
        "currency",
        "is_published",
    ]
    prepopulated_fields = {'slug': ('project_name',)}
    inlines = [OverheadViewInline, ImageInline, HousePointsInline, SchemaInline, InteriorImageInline,
               EquipmentOptionsInline, EquipmentButtonInline,
               ConstructionDescriptionInline, ConstructionImageInline]
    list_editable = ['is_published']
    search_fields = ["title", "project_name", "house_style"]
    ordering = ["title"]
    actions = [copy_selected_houses]


@admin.register(Styles)
class StyleAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(SortHouse)
class SortHouseAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Equipment_Types)
class EquipmentTypesAdmin(admin.ModelAdmin):
    list_display = ["equipment_type"]
