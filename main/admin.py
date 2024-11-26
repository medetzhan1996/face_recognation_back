from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке объектов
    list_display = ('last_name', 'first_name', 'second_name', 'gender', 'birth_date', 'workplace', 'id_document')
    list_display_links = ('last_name', 'first_name')
    list_filter = ('gender', 'birth_date', 'workplace')
    search_fields = ('first_name', 'last_name', 'second_name', 'id_document', 'workplace')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'birth_date'

    # Настройка формы редактирования
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'second_name', 'photo')
        }),
        ('Личная информация', {
            'fields': ('birth_date', 'gender', 'id_document', 'address')
        }),
        ('Дополнительно', {
            'fields': ('workplace',),
            'classes': ('collapse',),
        }),
    )

    # Отображение миниатюры фотографии
    def get_photo(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" style="width: 50px; height: 50px;" />'
        return "Нет фото"
    get_photo.short_description = "Фотография"
    get_photo.allow_tags = True
