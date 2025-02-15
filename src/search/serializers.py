from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import ArticleDocument


class ArticleESSerializer(DocumentSerializer):
    class Meta:
        document = ArticleDocument
        fields = [
            "title",
            "author",
            "slug",
            "description",
            "body",
            "created_at",
        ]
