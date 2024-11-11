from django.contrib import admin  # noqa: D100
from django.contrib.auth.admin import UserAdmin

from app.models import Article, UserProfile


class ArticleAdmin(admin.ModelAdmin):
    """Override Admin class for Article model."""

    list_display = ("title", "word_count", "status", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "content")
    date_hierarchy = "created_at"
    ordering = ["created_at"]  # noqa: RUF012
    readonly_fields = ("word_count","created_at", "updated_at")

class CustomUserAdmin(UserAdmin):
    """Override Admin class for User model."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        ("Information", {
            "classes": ("wide", "extrapretty" ),
            "fields": ("email", "password1", "password2"),
            }),
        ("Personal info", {
            "classes": ("wide", "extrapretty", "collapse"),
            "fields": ("first_name", "last_name")}),
        ("Permissions", {
            "classes": ("wide", "extrapretty"),
            "fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = ("last_login", "date_joined")


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(UserProfile, CustomUserAdmin)
