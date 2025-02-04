from rest_framework import routers

from .views import ProfileView

router = routers.SimpleRouter()
router.register(r"", ProfileView, basename="profile")


urlpatterns = [] + router.urls
