from django.core.management.base import BaseCommand
from core.models import SiteSettings
class Command(BaseCommand):
 help='Create default AKATSUKI site settings.'
 def handle(self,*args,**kwargs):
  obj,created=SiteSettings.objects.get_or_create(pk=1)
  self.stdout.write(self.style.SUCCESS('Default settings created.' if created else 'Settings already exist.'))
