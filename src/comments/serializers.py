from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["__all__"]

    # def to_internal_value(self, data):
    #     raw = data.copy()
    #     raw["user__id"] = self.context["request"].user.id
    #     return super().to_internal_value(raw)


class CommentListSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user_first_name",
            "article_title",
            "parent_comment",
            "content",
            "created_at",
            "updated_at",
        ]
