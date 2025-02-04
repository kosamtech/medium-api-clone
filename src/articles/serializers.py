import logging

from django.db import IntegrityError
from rest_framework import serializers

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer
from comments.serializers import CommentSerializer
from profiles.serializers import ProfileSerializer

from .models import Article, ArticleView, Clap

logger = logging.getLogger(__name__)


class TagListField(serializers.Field):
    def to_representation(self, value):
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tags")

        tag_objects = []
        for tag_name in data:
            tag = tag_name.strip()

            if not tag:
                continue
            tag_objects.append(tag)
        return tag_objects


class ArticleSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    banner_image = serializers.SerializerMethodField()
    estimated_reading_time = serializers.ReadOnlyField()
    tags = TagListField()
    views = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    bookmarks = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    claps_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_claps_count(self, obj):
        return obj.claps.count()

    def get_bookmarks(self, obj):
        bookmarks = Bookmark.objects.filter(article=obj)
        return BookmarkSerializer(bookmarks, many=True).data

    def get_bookmarks_count(self, obj):
        return Bookmark.objects.filter(article=obj).count()

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_views(self, obj):
        return ArticleView.objects.filter(article=obj).count()

    def get_banner_image(self, obj):
        if obj.banner_image:
            return obj.banner_image.url
        return None

    def get_created_at(self, obj):
        return obj.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%m/%d/%Y, %H:%M:%S")

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        user = self.context["request"].user
        validated_data.update({"author": user})
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)
        logger.info(
            f"article {validated_data.get('title')} created by {user.first_name}"
        )
        return article

    def update(self, instance, validated_data):
        try:
            tags = validated_data.pop("tags")
        except KeyError:
            raise serializers.ValidationError({"tags": ["this key should not be None"]})
        instance.tags.set(tags)
        return super().update(instance, validated_data)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "tags",
            "estimated_reading_time",
            "author_info",
            "views",
            "description",
            "body",
            "banner_image",
            "average_rating",
            "bookmarks",
            "bookmarks_count",
            "claps_count",
            "comments",
            "comments_count",
            "created_at",
            "updated_at",
        ]


class ClapListSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)

    class Meta:
        model = Clap
        fields = ["id", "user_first_name", "article_title"]


class ClapSerializer(serializers.ModelSerializer):
    article = serializers.UUIDField()

    class Meta:
        model = Clap
        fields = ["article"]

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
