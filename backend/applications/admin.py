from django.contrib import admin, messages
from django.db import IntegrityError, transaction
from django.http import FileResponse, Http404
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404
from .models import Application, EmailLog
from members.models import CoreMember
from core.emailing import send_promotion_email

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'department', 'year', 'domain', 'status', 'created_at')
    list_filter = ('status', 'domain', 'department', 'year', ('created_at', admin.DateFieldListFilter))
    search_fields = ('full_name', 'email', 'roll_number', 'department')
    ordering = ('-created_at',)
    list_per_page = 30
    readonly_fields = ('created_at', 'resume_link')
    actions = ('promote_to_core_member',)
    fieldsets = (
        ('Personal Information', {'fields': ('full_name', 'email', 'phone')}),
        ('Academic Information', {'fields': ('roll_number', 'department', 'year')}),
        ('Domain', {'fields': ('domain',)}),
        ('Skills & Experience', {'fields': ('skills', 'experience', 'why_akatsuki')}),
        ('Social Links', {'fields': ('github', 'linkedin')}),
        ('Resume', {'fields': ('resume_link',)}),
        ('Application Status', {'fields': ('status', 'consent')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )
    @admin.display(description='Private resume')
    def resume_link(self, obj):
        if not obj or not obj.resume: return '—'
        url = reverse('admin:application-resume', args=[obj.pk])
        return format_html('<a href="{}">Download PDF</a>', url)
    def get_urls(self):
        return [path('<int:pk>/resume/', self.admin_site.admin_view(self.download_resume), name='application-resume')] + super().get_urls()
    def download_resume(self, request, pk):
        obj = get_object_or_404(Application, pk=pk)
        try: return FileResponse(obj.resume.open('rb'), as_attachment=True, filename=f'AKATSUKI-{obj.pk}-resume.pdf', content_type='application/pdf')
        except (FileNotFoundError, OSError): raise Http404('Resume not found')
    @admin.action(description='Promote to Core Member')
    def promote_to_core_member(self, request, queryset):
        done = skipped = email_failed = 0
        for app in queryset:
            if app.status not in (Application.Status.SHORTLISTED, Application.Status.ACCEPTED):
                skipped += 1; continue
            if CoreMember.objects.filter(email__iexact=app.email).exists():
                skipped += 1; continue
            try:
                with transaction.atomic():
                    member = CoreMember.objects.create(name=app.full_name, position='Core Member', domain=app.domain, bio=app.skills[:500], github=app.github, linkedin=app.linkedin, email=app.email)
                    app.status = Application.Status.CORE_MEMBER
                    app.save(update_fields=['status'])
            except IntegrityError:
                skipped += 1
                continue
            if not send_promotion_email(app, member): email_failed += 1
            done += 1
        if done: self.message_user(request, f'{done} applicant(s) promoted.', messages.SUCCESS)
        if skipped: self.message_user(request, f'{skipped} skipped because they are not shortlisted/accepted or already have a Core Member record.', messages.WARNING)
        if email_failed: self.message_user(request, f'{email_failed} email(s) failed. Review Email Logs and retry.', messages.WARNING)

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'email_type', 'status', 'sent_at')
    list_filter = ('status', 'email_type', 'sent_at')
    search_fields = ('recipient', 'subject')
    readonly_fields = ('recipient', 'subject', 'email_type', 'status', 'error_message', 'sent_at', 'related_application', 'related_member')
    actions = ('retry_failed',)
    @admin.action(description='Retry failed promotion email')
    def retry_failed(self, request, queryset):
        retried = 0
        for log in queryset.filter(status=EmailLog.State.FAILED, related_application__isnull=False, related_member__isnull=False):
            if send_promotion_email(log.related_application, log.related_member): retried += 1
        self.message_user(request, f'{retried} email(s) sent.' if retried else 'No failed promotion emails were sent.', messages.SUCCESS if retried else messages.WARNING)

admin.site.site_header = 'AKATSUKI Operations'
admin.site.site_title = 'AKATSUKI Admin'
admin.site.index_title = 'Club management'





