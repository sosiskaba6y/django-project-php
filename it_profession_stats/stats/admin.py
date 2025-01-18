from django.contrib import admin
from .models import PageCategory, PageContent

@admin.register(PageCategory)
class PageCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_tag')
    search_fields = ['title']
    list_filter = ['category']

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" height="100" />'
        return ''
    image_tag.short_description = 'Image Preview'
    image_tag.allow_tags = True