from django.contrib import admin
from application.models import ApplicationFile, Application, Cost_Application


class ApplicationFileInline(admin.TabularInline):
    model = ApplicationFile
    extra = 1


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["name", "number", "messenger", "created_time", "message"]
    inlines = [ApplicationFileInline]

    def has_add_permission(self, request):
        return False  # Запретить добавление новых заявок

    def has_change_permission(self, request, obj=None):
        return True  # Разрешить изменение существующих заявок

    def has_delete_permission(self, request, obj=None):
        return True  # Разрешить удаление существующих заявок

    def get_inline_instances(self, request, obj=None):
        # Отображаем только файлы, связанные с текущей заявкой
        if obj:
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        return []

    def get_files(self, obj):
        # Пользовательский метод для отображения файлов в списке
        return "\n".join([file.file.url for file in obj.applicationfile_set.all()])

    get_files.short_description = "Связанные файлы"  # Заголовок для столбца файлов

    list_display = ["application_number", "name", "number", "messenger", "created_time", "message", "get_files"]


@admin.register(Cost_Application)
class CostApplicationAdmin(admin.ModelAdmin):

    list_display = [

        "cost_application_number",
        "name",
        "number",
        "country",
        "city",
        "types_of_service",
        "types_of_payment"
    ]

    def has_add_permission(self, request):
        return False  # Запретить добавление новых заявок

    def has_change_permission(self, request, obj=None):
        return True  # Разрешить изменение существующих заявок

    def has_delete_permission(self, request, obj=None):
        return True  # Разрешить удаление существующих заявок
