"""Views for the app."""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from app.models import Article


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    """View for the list of Articles."""

    model = Article
    template_name = "app/home.html"
    context_object_name = "articles"

    def get_queryset(self) -> QuerySet[Any]:
        """Override get_queryset to filter by creator."""
        return Article.objects.filter(creator=self.request.user).order_by("-created_at")

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """View for creating an Article."""

    model = Article
    template_name = "app/article_create.html"
    fields = ["title", "content", "twitter_post", "status"]  # noqa: RUF012
    success_url = reverse_lazy("home")

    def form_valid(self, form):  # noqa: ANN001, ANN201
        """Override form_valid to set the creator field."""
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an Article."""

    model = Article
    template_name = "app/article_update.html"
    fields = ["title", "content",  "twitter_post", "status"]  # noqa: RUF012
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def test_func(self) -> bool:
        """Override test_func to check if the user is the creator of the Article."""
        return self.request.user == self.get_object().creator


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting an Article."""

    model = Article
    template_name = "app/article_delete.html"
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def test_func(self) -> bool:
        """Override test_func to check if the user is the creator of the Article."""
        return self.request.user == self.get_object().creator
