from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SiteSettings
class SettingsView(APIView):
 def get(self,request):
  s=SiteSettings.objects.first()
  if not s: return Response({'club_name':'AKATSUKI','tagline':'Build beyond the expected.','contact_email':'hello@akatsuki.club','instagram_url':'','linkedin_url':'','github_url':'','discord_url':'','college_name':'','footer_text':'Student technology community. Built by curious minds.'})
  return Response({k:getattr(s,k) for k in ('club_name','tagline','contact_email','instagram_url','linkedin_url','github_url','discord_url','college_name','footer_text')})
