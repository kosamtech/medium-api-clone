from django.db import IntegrityError
from rest_framework import serializers

from .models import Article, Bookmark


class BookmarkListSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "user_first_name", "article_title", "created_at", "updated_at"]
        read_only_fields = ["user"]


class BookmarkSerializer(serializers.ModelSerializer):
    article = serializers.UUIDField()

    class Meta:
        model = Bookmark
        fields = [
            "article",
        ]

    def create(self, validated_data):
        try:
            article = Article.objects.get(id=validated_data["article"])
        except Article.DoesNotExist:
            raise serializers.ValidationError({"error": "Article does not exist"})
        validated_data.update(
            {"article": article, "user": self.context["request"].user}
        )
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {"errors": "article and user need to be unique entries"}
            )
