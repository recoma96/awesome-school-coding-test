from django.db import models
from django.db.models import Q

class CourseEnrollmentStatus(models.TextChoices):
    PENDING = "PENDING", "신청 접수"
    IN_REVIEW = "IN_REVIEW", "확인중"
    APPROVED = "APPROVED", "접수 완료"
    CANCELED = "CANCELED", "취소"
    REJECT = "REJECT", "반려"  # 고객이 아닌 내부에서 신청 부적격으로 판단했을 경우
    COMPLETED = "COMPLETED", "수강 완료"



IN_PROGRESS_STATUSES = (
    CourseEnrollmentStatus.PENDING,
    CourseEnrollmentStatus.IN_REVIEW,
    CourseEnrollmentStatus.APPROVED,
)


class CourseEnrollment(models.Model):
    class Meta:
        db_table = "course_enrollment"
        verbose_name = "교육 신청 내역"
        verbose_name_plural = "교육 신청 목록"
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=Q(status__in=IN_PROGRESS_STATUSES),
                name="unique_in_progress_enrollment_per_email",
                violation_error_message="이미 진행 중인 신청 내역이 있습니다.",
            ),
        ]

    name = models.CharField(max_length=16, verbose_name="신청자 이름")
    available_connection_date = models.DateField(verbose_name="연락 가능 날짜")
    email = models.EmailField(verbose_name="신청자 이메일")
    address = models.CharField(max_length=256, verbose_name="신청자 주소")
    status = models.CharField(
        max_length=16, choices=CourseEnrollmentStatus.choices, verbose_name="신청 상태"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="신청날짜")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정날짜")

    def __str__(self):
        return f"({self.id}) {self.name} {self.email}"
