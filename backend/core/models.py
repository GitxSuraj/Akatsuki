from django.db import models
class SiteSettings(models.Model):
 club_name=models.CharField(max_length=100,default='AKATSUKI'); tagline=models.CharField(max_length=200,default='Build beyond the expected.'); contact_email=models.EmailField(default='teamakatsukibots@gmail.com'); instagram_url=models.URLField(blank=True); linkedin_url=models.URLField(blank=True); github_url=models.URLField(blank=True); discord_url=models.URLField(blank=True); college_name=models.CharField(max_length=200,blank=True); footer_text=models.CharField(max_length=250,default='Student technology community. Built by curious minds.')
 class Meta: verbose_name_plural='site settings'
 def __str__(self): return self.club_name

