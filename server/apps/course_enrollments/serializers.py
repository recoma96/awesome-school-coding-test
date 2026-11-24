from datetime import date

from rest_framework import serializers
from django.utils import timezone

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

    def validate_available_connection_date(self, value: date) -> date:
        print(type(value))
        if value <= timezone.localdate():
            raise serializers.ValidationError("연락 가능 날짜는 내일 이후로 선택해주세요.")
        return value
