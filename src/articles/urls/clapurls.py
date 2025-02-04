from rest_framework.routers import SimpleRouter

from articles.views import ClapArticleView

router = SimpleRouter()
router.register(r"", ClapArticleView, basename="clap")


urlpatterns = [] + router.urls
