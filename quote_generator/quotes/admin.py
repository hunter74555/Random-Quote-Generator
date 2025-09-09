from django.contrib import admin
from .models import Source, Quote


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'created_at']
    list_filter = ['type']
    search_fields = ['name']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text_short', 'source', 'weight', 'views', 'likes', 'dislikes', 'created_at']
    list_filter = ['source__type', 'created_at']
    search_fields = ['text', 'source__name']
    list_editable = ['weight']

    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_short.short_description = 'Текст'