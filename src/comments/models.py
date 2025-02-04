from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from articles.models import Article
from common.models import TimestampedModel

User = get_user_model()


class Comment(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="replies"
    )
    content = models.TextField(verbose_name=_("comment content"))

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.first_name} commented on {self.article.title}"
