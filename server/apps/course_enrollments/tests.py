from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CourseEnrollment, CourseEnrollmentStatus, IN_PROGRESS_STATUSES


class CourseEnrollmentCreateAPITest(APITestCase):
    url = reverse("course-enrollment-list")

    # API는 camelCase로 받는다.
    payload = {
        "name": "홍길동",
        "availableConnectionDate": "2026-12-01",
        "email": "hong@example.com",
        "address": "서울특별시 강남구",
    }

    def create_enrollment(self, enrollment_status: str) -> CourseEnrollment:
        """기존 신청 내역을 DB에 직접 만든다."""
        return CourseEnrollment.objects.create(
            name=self.payload["name"],
            available_connection_date=self.payload["availableConnectionDate"],
            email=self.payload["email"],
            address=self.payload["address"],
            status=enrollment_status,
        )

    def test_create_success(self):
        response = self.client.post(self.url, self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        enrollment = CourseEnrollment.objects.get()
        self.assertEqual(enrollment.id, response.data["id"])
        self.assertEqual(enrollment.email, self.payload["email"])
        self.assertEqual(enrollment.status, CourseEnrollmentStatus.PENDING)

    def test_create_ignores_client_status(self):
        """클라이언트가 status를 보내도 PENDING으로 저장된다."""
        payload = {**self.payload, "status": CourseEnrollmentStatus.APPROVED}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        enrollment = CourseEnrollment.objects.get()
        self.assertEqual(enrollment.status, CourseEnrollmentStatus.PENDING)

    def test_create_duplicated_when_in_progress(self):
        """같은 이메일로 진행 중(PENDING/IN_REVIEW/APPROVED)인 신청이 있으면 거부된다."""
        in_progress_statuses = (
            CourseEnrollmentStatus.PENDING,
            CourseEnrollmentStatus.IN_REVIEW,
            CourseEnrollmentStatus.APPROVED,
        )
        for enrollment_status in in_progress_statuses:
            with self.subTest(status=enrollment_status):
                CourseEnrollment.objects.all().delete()
                self.create_enrollment(enrollment_status)

                response = self.client.post(self.url, self.payload, format="json")

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(
                    response.data["non_field_errors"],
                    ["이미 진행 중인 신청 내역이 있습니다."],
                )
                self.assertEqual(CourseEnrollment.objects.count(), 1)

    def test_create_allowed_when_previous_closed(self):
        """같은 이메일이어도 이전 신청이 취소/반려/완료라면 새로 신청할 수 있다."""
        closed_statuses = (
            CourseEnrollmentStatus.CANCELED,
            CourseEnrollmentStatus.REJECT,
            CourseEnrollmentStatus.COMPLETED,
        )

        for enrollment_status in closed_statuses:
            with self.subTest(status=enrollment_status):
                CourseEnrollment.objects.all().delete()
                self.create_enrollment(enrollment_status)

                response = self.client.post(self.url, self.payload, format="json")

                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(
                    CourseEnrollment.objects.filter(
                        email=self.payload["email"],
                        status=CourseEnrollmentStatus.PENDING,
                    ).count(),
                    1,
                )
