from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible

@deconstructible
class PrivateResumeStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('location', settings.BASE_DIR / 'private-media' / 'resumes')
        kwargs.setdefault('base_url', None)
        super().__init__(*args, **kwargs)
