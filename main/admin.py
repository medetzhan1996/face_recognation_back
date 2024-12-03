from django.contrib import admin
from .models import Client
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    class Media:
        js = ('js/camera.js',)



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке объектов
    list_display = ('name',)
    search_fields = ('name', )
    form = ClientAdminForm

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields += ('name', 'photo')
        return readonly_fields

    # Отображение миниатюры фотографии
    def get_photo(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" style="width: 50px; height: 50px;" />'
        return "Нет фото"
    get_photo.short_description = "Фотография"
    get_photo.allow_tags = True


admin.site.unregister(Group)
admin.site.unregister(User)