from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from members.views import MemberViewSet
from events.views import EventViewSet
from gallery.views import GalleryViewSet
from core.views import SettingsView
from applications.views import ApplicationViewSet
router=DefaultRouter()
router.register('members',MemberViewSet,basename='member'); router.register('events',EventViewSet,basename='event'); router.register('gallery',GalleryViewSet,basename='gallery'); router.register('applications',ApplicationViewSet,basename='application')
urlpatterns=[path('admin/',admin.site.urls),path('api/',include(router.urls)),path('api/settings/',SettingsView.as_view())]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
