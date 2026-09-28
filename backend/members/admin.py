from django.contrib import admin
from .models import CoreMember
@admin.register(CoreMember)
class CoreMemberAdmin(admin.ModelAdmin): list_display=('name','position','domain','is_active','display_order'); list_filter=('domain','is_active'); search_fields=('name','position','email'); list_editable=('is_active','display_order'); ordering=('display_order','name')
