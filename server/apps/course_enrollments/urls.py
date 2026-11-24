from rest_framework.routers import SimpleRouter

from .views import CourseEnrollmentsViewSet

router = SimpleRouter()
router.register("", CourseEnrollmentsViewSet, basename="course-enrollment")

urlpatterns = router.urls
