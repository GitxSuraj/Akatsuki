from rest_framework import serializers,viewsets
from rest_framework.permissions import AllowAny
from .models import CoreMember
class MemberSerializer(serializers.ModelSerializer):
 photo=serializers.ImageField(use_url=True)
 class Meta: model=CoreMember; fields=('id','name','photo','position','domain','bio','github','linkedin','email')
class MemberViewSet(viewsets.ReadOnlyModelViewSet):
 serializer_class=MemberSerializer; permission_classes=[AllowAny]; pagination_class=None
 def get_queryset(self): return CoreMember.objects.filter(is_active=True).order_by('display_order','name')
