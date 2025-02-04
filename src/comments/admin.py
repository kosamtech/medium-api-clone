from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "user", "article", "created_at"]
    list_display_links = ["pkid", "id", "user"]


admin.site.register(Comment, CommentAdmin)
