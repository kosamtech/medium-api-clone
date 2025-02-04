from rest_framework.routers import SimpleRouter

from .views import ArticleElasticSearchView

router = SimpleRouter()
router.register(r"search", ArticleElasticSearchView, basename="article-search")

urlpatterns = [] + router.urls
