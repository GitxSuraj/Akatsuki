from django.contrib import admin
from .models import GalleryImage
@admin.register(GalleryImage)
class GalleryAdmin(admin.ModelAdmin): list_display=('caption','event','display_order','is_visible','uploaded_at'); list_filter=('is_visible','event'); search_fields=('caption',); list_editable=('display_order','is_visible'); ordering=('display_order',)
