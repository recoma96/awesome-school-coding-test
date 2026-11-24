from typing import Dict, Any

from rest_framework import serializers

from .models import CourseEnrollment, CourseEnrollmentStatus


class CourseEnrollmentsSerializer(serializers.ModelSerializer):
    status = serializers.HiddenField(default=CourseEnrollmentStatus.PENDING)

    class Meta:
        model = CourseEnrollment
        fields = (
            "id",
            "name",
            "available_connection_date",
            "email",
            "address",
            "status",
        )
