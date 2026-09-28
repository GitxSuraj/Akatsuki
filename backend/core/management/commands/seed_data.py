from django.core.management.base import BaseCommand
from core.models import SiteSettings
from members.models import CoreMember
TEAM = (
 {'name':'Suraj Kumar','position':'Core Member','domain':CoreMember.Domain.SOFTWARE,'github':'https://github.com/GitxSuraj','linkedin':'https://www.linkedin.com/in/carteacan/','instagram':'https://www.instagram.com/suraj.sha.rma/','display_order':1},
 {'name':'Devesh Kumar','position':'Core Member','domain':CoreMember.Domain.HARDWARE,'linkedin':'https://www.linkedin.com/in/devesh-kumar-4056b7274/','instagram':'https://www.instagram.com/spidermanfromwalmart/','display_order':2},
)
class Command(BaseCommand):
 help='Create the AKATSUKI site settings and supplied core team profiles.'
 def handle(self,*args,**kwargs):
  settings,_=SiteSettings.objects.get_or_create(pk=1)
  if settings.contact_email in ('','hello@akatsuki.club'):
   settings.contact_email='teamakatsukibots@gmail.com'; settings.save(update_fields=['contact_email'])
  added=0
  for data in TEAM:
   _,created=CoreMember.objects.get_or_create(name=data['name'],defaults=data); added+=created
  self.stdout.write(self.style.SUCCESS(f'Site settings ready; {added} core team profile(s) added.'))
