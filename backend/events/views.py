from rest_framework import serializers,viewsets
from rest_framework.permissions import AllowAny
from .models import Event
class EventSerializer(serializers.ModelSerializer):
 class Meta: model=Event; fields=('id','title','description','image','date','location','registration_url')
class EventViewSet(viewsets.ReadOnlyModelViewSet):
 serializer_class=EventSerializer; permission_classes=[AllowAny]; pagination_class=None
 def get_queryset(self): return Event.objects.filter(is_published=True).order_by('-date')
