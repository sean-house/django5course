"""URLs for the app."""

from django.urls import path

from app.views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleListView,
    ArticleUpdateView,
    ArticleDetailView,
    PublicListView,
)

urlpatterns = [
    path("", PublicListView.as_view(), name="home"),
    path("authors/", ArticleListView.as_view(), name="authors"),
    path("create/", ArticleCreateView.as_view(), name="create_article"),
    path("<int:pk>/view/", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/update/", ArticleUpdateView.as_view(), name="update_article"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="delete_article"),
]
