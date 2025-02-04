from common.views import GenericModelViewSet

from .models import Rating
from .serializers import RatingListSerializer, RatingSerializer


class RatingView(GenericModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    action_serializers = {
        "list": RatingListSerializer,
        "retrieve": RatingListSerializer,
    }
