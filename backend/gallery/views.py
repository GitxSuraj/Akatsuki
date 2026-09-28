from django.db.models import Q
from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from .models import GalleryImage
class GallerySerializer(serializers.ModelSerializer):
    class Meta: model=GalleryImage; fields=('id','image','caption','event')
class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=GallerySerializer; permission_classes=[AllowAny]; pagination_class=None
    def get_queryset(self):
        return GalleryImage.objects.filter(Q(event__isnull=True)|Q(event__is_published=True),is_visible=True).order_by('display_order','-uploaded_at')
