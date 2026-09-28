from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from .models import Application

class ApplicationWriteSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(use_url=False)
    class Meta:
        model = Application
        fields = ('full_name','email','phone','roll_number','department','year','domain','skills','experience','github','linkedin','why_akatsuki','resume','consent')
    def validate_resume(self, uploaded):
        if uploaded.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Resume must be 5 MB or smaller.')
        if not uploaded.name.lower().endswith('.pdf') or uploaded.content_type not in ('application/pdf','application/x-pdf'):
            raise serializers.ValidationError('Upload a PDF resume.')
        header = uploaded.read(5)
        uploaded.seek(0)
        if header != b'%PDF-':
            raise serializers.ValidationError('The selected file is not a valid PDF.')
        return uploaded
    def validate_consent(self, value):
        if not value: raise serializers.ValidationError('Please confirm the information is accurate.')
        return value
    def validate(self, attrs):
        since = timezone.now() - timedelta(days=30)
        if Application.objects.filter(email__iexact=attrs.get('email','').strip(), created_at__gte=since).exists():
            raise serializers.ValidationError({'email':'An application was recently submitted with this email.'})
        return attrs

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'application'
    def get_permissions(self): return [AllowAny()] if self.action == 'create' else [IsAdminUser()]
    def get_serializer_class(self): return ApplicationWriteSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'detail':'Please review the highlighted fields.','errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'message':'Application received.','status':'PENDING'}, status=status.HTTP_201_CREATED)

