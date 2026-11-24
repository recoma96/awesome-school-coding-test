from rest_framework import viewsets, mixins

from .models import CourseEnrollment
from .serializers import CourseEnrollmentsSerializer


class CourseEnrollmentsViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = CourseEnrollment.objects.all()
    serializer_class = CourseEnrollmentsSerializer
    authentication_classes = []
