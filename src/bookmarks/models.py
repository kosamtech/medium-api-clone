from django.contrib.auth import get_user_model
from django.db import models

from articles.models import Article
from common.models import TimestampedModel

User = get_user_model()


class Bookmark(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="bookmarks"
    )

    class Meta:
        unique_together = ["user", "article"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.first_name} bookmarked {self.article.title}"
