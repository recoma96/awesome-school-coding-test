from rest_framework.routers import SimpleRouter

from .views import CourseEnrollmentsViewSet

router = SimpleRouter()
router.register("", CourseEnrollmentsViewSet)

urlpatterns = router.urls
