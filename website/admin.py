from django.contrib import admin
from .models import LocationMarker

@admin.register(LocationMarker)
class LocationMarkerAdmin(admin.ModelAdmin):
    list_display = ('location', 'description', 'tel', 'latitude', 'longitude')
    search_fields = ('location', 'description')
    list_filter = ('location',)
    ordering = ('location',)
    
    # Optional: Add fieldsets for better organization
    fieldsets = (
        (None, {
            'fields': ('location', 'description')
        }),
        ('Contact Details', {
            'fields': ('tel', 'link')
        }),
        ('Coordinates', {
            'fields': ('latitude', 'longitude')
        }),
    )