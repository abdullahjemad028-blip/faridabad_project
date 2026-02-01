from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'event_time', 'venue', 'is_active']
    list_filter = ['is_active', 'event_date']
    search_fields = ['title', 'description', 'venue']
    list_editable = ['is_active']
    date_hierarchy = 'event_date'
