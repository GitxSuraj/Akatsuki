from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.conf import settings
from applications.models import EmailLog
SUBJECT='Congratulations! Welcome to the AKATSUKI Core Team'
def send_promotion_email(application, member):
 html=f'''<!doctype html><html><body style="margin:0;background:#080808;color:#f5f5f5;font-family:Arial,sans-serif"><div style="max-width:600px;margin:32px auto;border:1px solid #332027;background:#111;padding:38px"><div style="color:#e10600;font-size:13px;letter-spacing:5px;font-weight:bold">AKATSUKI</div><h1 style="font-size:30px;margin:24px 0 12px">Congratulations, {member.name}.</h1><p style="color:#ddd;line-height:1.7">You have been selected as a Core Member of AKATSUKI. You are now officially part of the team building across technology, robotics and artificial intelligence.</p><div style="border-left:3px solid #e10600;padding:12px 18px;margin:24px 0;color:#fff"><b>{member.domain}</b>{f' · {member.position}' if member.position else ''}</div><p style="color:#ddd;line-height:1.7">Welcome to AKATSUKI. We look forward to building, learning and innovating together.</p><div style="color:#888;font-size:12px;margin-top:32px">Student technology community · Build beyond the expected.</div></div></body></html>'''
 text=f'Dear {member.name},\n\nCongratulations! You have been selected as a Core Member of AKATSUKI ({member.domain}).\n\nWelcome to AKATSUKI. We look forward to building, learning and innovating together.'
 try:
  mail=EmailMultiAlternatives(SUBJECT,text,settings.DEFAULT_FROM_EMAIL,[application.email]); mail.attach_alternative(html,'text/html'); mail.send(fail_silently=False)
  EmailLog.objects.create(recipient=application.email,subject=SUBJECT,email_type='CORE_PROMOTION',status=EmailLog.State.SENT,sent_at=timezone.now(),related_application=application,related_member=member)
  return True
 except Exception as exc:
  EmailLog.objects.create(recipient=application.email,subject=SUBJECT,email_type='CORE_PROMOTION',status=EmailLog.State.FAILED,error_message=str(exc)[:4000],related_application=application,related_member=member)
  return False

