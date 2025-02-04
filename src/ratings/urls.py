from rest_framework.routers import SimpleRouter

from .views import RatingView

router = SimpleRouter()
router.register(r"", RatingView, basename="rating")

urlpatterns = [] + router.urls
