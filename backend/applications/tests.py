from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from members.models import CoreMember
from events.models import Event
from applications.models import Application
from gallery.models import GalleryImage
from core.models import SiteSettings
from core.emailing import send_promotion_email
from datetime import timedelta
from django.utils import timezone
class PublicApiTests(TestCase):
 def test_public_member_endpoint_only_returns_active_members(self):
  CoreMember.objects.create(name='Visible',position='Lead',domain='HARDWARE',is_active=True)
  CoreMember.objects.create(name='Hidden',position='Lead',domain='SOFTWARE',is_active=False)
  response=APIClient().get('/api/members/')
  self.assertEqual(response.status_code,200); self.assertEqual([x['name'] for x in response.json()],['Visible'])
 def test_private_applications_are_not_publicly_listed(self):
  response=APIClient().get('/api/applications/')
  self.assertIn(response.status_code,(401,403))
 def test_site_settings_has_public_defaults(self):
  self.assertEqual(APIClient().get('/api/settings/').json()['club_name'],'AKATSUKI')
class ApplicationValidationTests(TestCase):
 def payload(self,email='applicant@example.edu'):
  return {'full_name':'Test Applicant','email':email,'phone':'1234567890','roll_number':'A-42','department':'Engineering','year':'2nd Year','domain':'SOFTWARE','skills':'Python','experience':'','github':'','linkedin':'','why_akatsuki':'I like building','consent':'true','resume':SimpleUploadedFile('resume.pdf',b'%PDF-1.4 sample',content_type='application/pdf')}
 def test_application_submission_saves_pending_application(self):
  response=APIClient().post('/api/applications/',self.payload(),format='multipart')
  self.assertEqual(response.status_code,201); self.assertEqual(Application.objects.get().status,'PENDING')
 def test_recent_duplicate_email_is_rejected(self):
  app=Application.objects.create(full_name='Existing',email='applicant@example.edu',phone='1',roll_number='1',department='Engineering',year='2',domain='SOFTWARE',skills='Python',why_akatsuki='Build',consent=True,resume=SimpleUploadedFile('resume.pdf',b'%PDF',content_type='application/pdf'))
  response=APIClient().post('/api/applications/',self.payload(),format='multipart')
  self.assertEqual(response.status_code,400); app.resume.delete(save=False)
 def test_invalid_resume_is_rejected(self):
  p=self.payload(); p['resume']=SimpleUploadedFile('notes.txt',b'not pdf',content_type='text/plain')
  self.assertEqual(APIClient().post('/api/applications/',p,format='multipart').status_code,400)
class PromotionTests(TestCase):
 def test_promotion_email_is_logged_on_success(self):
  from applications.models import EmailLog
  from applications.admin import ApplicationAdmin
  from django.contrib.admin.sites import AdminSite
  from django.contrib.auth import get_user_model
  from django.contrib.messages.storage.fallback import FallbackStorage
  from django.test import RequestFactory
  app=Application.objects.create(full_name='Alex Example',email='alex@example.edu',phone='1',roll_number='1',department='Engineering',year='2',domain='HARDWARE',skills='Robotics',why_akatsuki='Build',consent=True,status='ACCEPTED',resume=SimpleUploadedFile('resume.pdf',b'%PDF',content_type='application/pdf'))
  request=RequestFactory().post('/admin/'); request.user=get_user_model().objects.create_superuser('admin','admin@example.edu','unused'); request.session={}; request._messages=FallbackStorage(request)
  with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
   ApplicationAdmin(Application,AdminSite()).promote_to_core_member(request,Application.objects.filter(pk=app.pk))
  app.refresh_from_db(); self.assertEqual(app.status,'CORE_MEMBER'); self.assertEqual(CoreMember.objects.filter(email='alex@example.edu').count(),1); self.assertEqual(EmailLog.objects.filter(status='SENT').count(),1)
 def test_duplicate_promotion_does_not_create_second_member(self):
  from applications.admin import ApplicationAdmin
  from django.contrib.admin.sites import AdminSite
  from django.contrib.auth import get_user_model
  from django.contrib.messages.storage.fallback import FallbackStorage
  from django.test import RequestFactory
  app=Application.objects.create(full_name='Alex Example',email='alex@example.edu',phone='1',roll_number='1',department='Engineering',year='2',domain='HARDWARE',skills='Robotics',why_akatsuki='Build',consent=True,status='ACCEPTED',resume=SimpleUploadedFile('resume.pdf',b'%PDF',content_type='application/pdf'))
  CoreMember.objects.create(name=app.full_name,position='Lead',domain=app.domain,email=app.email)
  request=RequestFactory().post('/admin/'); request.user=get_user_model().objects.create_superuser('admin','admin@example.edu','unused'); request.session={}; request._messages=FallbackStorage(request)
  ApplicationAdmin(Application,AdminSite()).promote_to_core_member(request,Application.objects.filter(pk=app.pk))
  self.assertEqual(CoreMember.objects.filter(email=app.email).count(),1); self.assertEqual(app.status,'ACCEPTED')


 def test_pending_applications_are_not_promoted(self):
  from applications.admin import ApplicationAdmin
  from django.contrib.admin.sites import AdminSite
  from django.contrib.auth import get_user_model
  from django.contrib.messages.storage.fallback import FallbackStorage
  from django.test import RequestFactory
  app=Application.objects.create(full_name='Jordan Applicant',email='jordan@example.edu',phone='1',roll_number='2',department='Engineering',year='1',domain='SOFTWARE',skills='AI',why_akatsuki='Learn',consent=True)
  request=RequestFactory().post('/admin/'); request.user=get_user_model().objects.create_superuser('admin2','admin2@example.edu','unused'); request.session={}; request._messages=FallbackStorage(request)
  ApplicationAdmin(Application,AdminSite()).promote_to_core_member(request,Application.objects.filter(pk=app.pk))
  self.assertEqual(app.status,'PENDING'); self.assertFalse(CoreMember.objects.filter(email=app.email).exists())
 def test_failed_email_is_logged_without_crashing(self):
  from applications.models import EmailLog
  from members.models import CoreMember
  from unittest.mock import patch
  app=Application.objects.create(full_name='Sam Example',email='sam@example.edu',phone='1',roll_number='3',department='Engineering',year='3',domain='SOFTWARE',skills='ML',why_akatsuki='Build',consent=True,status='ACCEPTED')
  member=CoreMember.objects.create(name=app.full_name,position='AI Lead',domain=app.domain,email=app.email)
  with patch('core.emailing.EmailMultiAlternatives.send',side_effect=OSError('SMTP unavailable')):
   self.assertFalse(send_promotion_email(app,member))
  log=EmailLog.objects.get(related_application=app)
  self.assertEqual(log.status,'FAILED'); self.assertIn('SMTP unavailable',log.error_message)
