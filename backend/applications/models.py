from django.db import models
from django.core.validators import FileExtensionValidator
from .storage import PrivateResumeStorage
from django.conf import settings
from pathlib import Path
private_resume_storage=PrivateResumeStorage()
class Application(models.Model):
 class Domain(models.TextChoices): HARDWARE='HARDWARE','Hardware'; SOFTWARE='SOFTWARE','Software'
 class Status(models.TextChoices): PENDING='PENDING','Pending'; SHORTLISTED='SHORTLISTED','Shortlisted'; ACCEPTED='ACCEPTED','Accepted'; REJECTED='REJECTED','Rejected'; CORE_MEMBER='CORE_MEMBER','Core member'
 full_name=models.CharField(max_length=160); email=models.EmailField(db_index=True); phone=models.CharField(max_length=30); roll_number=models.CharField(max_length=60); department=models.CharField(max_length=120); year=models.CharField(max_length=30); domain=models.CharField(max_length=10,choices=Domain.choices); skills=models.TextField(); experience=models.TextField(blank=True); github=models.URLField(blank=True); linkedin=models.URLField(blank=True); why_akatsuki=models.TextField(); resume=models.FileField(upload_to='',storage=private_resume_storage,validators=[FileExtensionValidator(['pdf'])]); consent=models.BooleanField(default=False); status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=('-created_at',)
 def __str__(self): return f'{self.full_name} — {self.domain}'
class EmailLog(models.Model):
 class State(models.TextChoices): SENT='SENT','Sent'; FAILED='FAILED','Failed'
 recipient=models.EmailField(); subject=models.CharField(max_length=250); email_type=models.CharField(max_length=80); status=models.CharField(max_length=10,choices=State.choices); error_message=models.TextField(blank=True); sent_at=models.DateTimeField(null=True,blank=True); related_application=models.ForeignKey(Application,on_delete=models.SET_NULL,null=True,blank=True,related_name='email_logs'); related_member=models.ForeignKey('members.CoreMember',on_delete=models.SET_NULL,null=True,blank=True,related_name='email_logs')
 class Meta: ordering=('-sent_at','-pk')
 def __str__(self): return f'{self.email_type} to {self.recipient}: {self.status}'

