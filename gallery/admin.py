from django.contrib import admin
from .models import GalleryCategory, GalleryImage

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date_taken', 'is_featured']
    list_filter = ['category', 'is_featured', 'date_taken']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    date_hierarchy = 'date_taken'