import logging

from django.contrib.auth import get_user_model
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from common.views import GenericModelViewSet

from .filters import ArticleFilter
from .models import Article, ArticleView, Clap
from .serializers import ArticleSerializer, ClapListSerializer, ClapSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class ArticleViewSet(GenericModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filterset_class = ArticleFilter
    ordering_fields = ["created_at", "updated_at"]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        viewer_ip = request.META.get("REMOTE_ADDR", None)
        ArticleView.record_view(
            article=instance, user=request.user, viewer_ip=viewer_ip
        )
        return super().retrieve(request, *args, **kwargs)


class ClapArticleView(GenericModelViewSet):
    queryset = Clap.objects.all()
    serializer_class = ClapSerializer
    action_serializers = {
        "list": ClapListSerializer,
        "retrieve": ClapListSerializer,
    }
