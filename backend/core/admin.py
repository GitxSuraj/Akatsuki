from django.contrib import admin
from .models import SiteSettings
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display=('club_name','contact_email','college_name')
    fieldsets=((None,{'fields':('club_name','tagline','footer_text')}),('Contact & social',{'fields':('contact_email','instagram_url','linkedin_url','github_url','discord_url')}),('Institution',{'fields':('college_name',)}))
    def has_add_permission(self,request): return not SiteSettings.objects.exists() and super().has_add_permission(request)
