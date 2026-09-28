from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
class CoreMember(models.Model):
    class Domain(models.TextChoices):
        HARDWARE='HARDWARE','Hardware'
        SOFTWARE='SOFTWARE','Software'
    name=models.CharField(max_length=120)
    photo=models.ImageField(upload_to='members/',blank=True)
    position=models.CharField(max_length=120)
    domain=models.CharField(max_length=10,choices=Domain.choices)
    bio=models.TextField(blank=True)
    github=models.URLField(blank=True)
    linkedin=models.URLField(blank=True)
    instagram=models.URLField(blank=True)
    email=models.EmailField(blank=True)
    personal_email=models.EmailField(blank=True)
    is_active=models.BooleanField(default=True)
    display_order=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=('display_order','name')
        constraints=[models.UniqueConstraint(Lower('email'),condition=~Q(email=''),name='unique_core_member_email_ci')]
    def __str__(self): return f'{self.name} — {self.position}'
