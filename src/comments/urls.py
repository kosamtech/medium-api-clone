from rest_framework.routers import SimpleRouter

from .views import CommentView

router = SimpleRouter()
router.register(r"", CommentView, basename="comment")

urlpatterns = [] + router.urls
