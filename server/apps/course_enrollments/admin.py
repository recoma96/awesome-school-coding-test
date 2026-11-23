from django.contrib import admin

from .models import CourseEnrollment


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "status", "available_connection_date", "created_at")
    list_display_links = ("id", "name")
    list_filter = ("status",)
    search_fields = ("name", "email")
    ordering = ("-created_at",)
    list_per_page = 30

    # 상세(수정) 화면
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("신청자 정보", {"fields": ("name", "email", "address", "available_connection_date")}),
        ("처리 상태", {"fields": ("status",)}),
        ("신청 날짜", {"fields": ("created_at", "updated_at")}),
    )
