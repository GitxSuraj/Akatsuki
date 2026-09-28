from django.db import models
class Event(models.Model):
 title=models.CharField(max_length=180); description=models.TextField(); image=models.ImageField(upload_to='events/',blank=True); date=models.DateTimeField(); location=models.CharField(max_length=200); registration_url=models.URLField(blank=True); is_published=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 class Meta: ordering=('-date',)
 def __str__(self): return self.title
