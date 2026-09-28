from django.db import models
from events.models import Event
class GalleryImage(models.Model):
 image=models.ImageField(upload_to='gallery/'); caption=models.CharField(max_length=240,blank=True); event=models.ForeignKey(Event,on_delete=models.SET_NULL,null=True,blank=True,related_name='gallery_images'); display_order=models.PositiveIntegerField(default=0); is_visible=models.BooleanField(default=True); uploaded_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=('display_order','-uploaded_at')
 def __str__(self): return self.caption or f'Gallery image {self.pk}'
