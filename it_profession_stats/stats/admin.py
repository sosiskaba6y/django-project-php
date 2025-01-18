from django.contrib import admin
from .models import PageContent

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')  # Добавим отображение изображения в админке

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return ''
    image_tag.short_description = 'Image Preview'
    image_tag.allow_tags = True