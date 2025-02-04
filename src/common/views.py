from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .pagination import MediumPagination
from .renderers import MediumJSONRenderer


class GenericModelViewSet(ModelViewSet):
    renderer_classes = (MediumJSONRenderer,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    action_serializers = {}
    pagination_class = MediumPagination

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class` for
        create, update & partial_update actions
        """
        serializer = self.action_serializers.get(self.action)
        if serializer:
            return serializer
        return super().get_serializer_class()
