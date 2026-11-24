from .base import *

from django.core.exceptions import ImproperlyConfigured


ENABLE_API_DOCS = True

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS 환경변수를 설정해야 합니다. (예: example.com,www.example.com)")
