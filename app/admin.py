from django.contrib import admin  # noqa: D100

from app.models import Article, UserProfile


class ArticleAdmin(admin.ModelAdmin):
    """Override Admin class for Article model."""

    list_display = ("title", "word_count", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ["created_at"]  # noqa: RUF012
    readonly_fields = ("word_count","created_at", "updated_at")


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(UserProfile)
