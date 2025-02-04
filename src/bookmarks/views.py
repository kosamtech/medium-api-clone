from rest_framework import status
from rest_framework.response import Response

from common.views import GenericModelViewSet

from .models import Bookmark
from .serializers import BookmarkListSerializer, BookmarkSerializer


class BookmarkView(GenericModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    action_serializers = {
        "list": BookmarkListSerializer,
        "retrieve": BookmarkListSerializer,
    }

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            return Response(
                {"message": "You cannot delete a bookmark that is not yours"},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()
        return Response(
            {"message": "bookmark deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
