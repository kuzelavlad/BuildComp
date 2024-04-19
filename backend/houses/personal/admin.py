from django.contrib import admin
from personal.models import Personal


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ["name", "department", "position"]