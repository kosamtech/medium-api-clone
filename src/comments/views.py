from rest_framework import status
from rest_framework.response import Response

from common.views import GenericModelViewSet

from .models import Comment
from .serializers import CommentListSerializer, CommentSerializer


class CommentView(GenericModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    action_serializers = {
        "list": CommentListSerializer,
        "retrieve": CommentListSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            return Response(
                {"message": "You don't have the permission to edit this comment"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != self.get_object().user:
            return Response(
                {"message": "You don't have the permission to delete this comment"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().perform_destroy(instance)
