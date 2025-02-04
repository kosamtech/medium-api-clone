from rest_framework.routers import SimpleRouter

from articles.views import ArticleViewSet

router = SimpleRouter()
router.register(r"", ArticleViewSet, basename="article")


urlpatterns = [] + router.urls
