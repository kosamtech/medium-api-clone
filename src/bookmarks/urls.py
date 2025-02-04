from rest_framework.routers import SimpleRouter

from .views import BookmarkView

router = SimpleRouter()
router.register(r"", BookmarkView, basename="bookmark")

urlpatterns = [] + router.urls
