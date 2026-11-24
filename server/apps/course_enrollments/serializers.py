from typing import Dict, Any

from rest_framework import serializers

from .models import CourseEnrollment, CourseEnrollmentStatus, IN_PROGRESS_STATUSES


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

    def validate(self, attr: Dict[str, Any]) -> Dict[str, Any]:
        is_duplicated = CourseEnrollment.objects.filter(
            email=attr["email"],
            status__in=IN_PROGRESS_STATUSES,
        ).exists()
        if is_duplicated:
            raise serializers.ValidationError(
                {"email": "이미 진행 중인 신청 내역이 있습니다."}
            )
        return attr
