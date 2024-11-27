"""Views for the app."""

import markdown
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView

from app.models import Article


# Create your views here.

class PublicListView(ListView):
    """View for the public list of Articles."""

    model = Article
    template_name = "app/public.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        """Override get_queryset to filter by creator."""
        search = self.request.GET.get("search")
        queryset = super().get_queryset().filter(status="published")
        if search:
            queryset = queryset.filter(title__search=search)
        return queryset.order_by("-created_at")

class ArticleListView(LoginRequiredMixin, ListView):
    """View for the list of Articles."""

    model = Article
    template_name = "app/authors.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        """Override get_queryset to filter by creator."""
        search = self.request.GET.get("search")
        queryset = super().get_queryset().filter(creator=self.request.user)
        if search:
            queryset = queryset.filter(title__search=search)
        return queryset.order_by("-created_at")

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """View for creating an Article."""

    model = Article
    template_name = "app/article_create.html"
    fields = ["title", "content", "twitter_post", "status"]  # noqa: RUF012
    success_url = reverse_lazy("authors")

    def form_valid(self, form):  # noqa: ANN001, ANN201
        """Override form_valid to set the creator field."""
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    """View for updating an Article."""

    model = Article
    template_name = "app/article_view.html"
    fields = ["title", "content",  "twitter_post", "status"]  # noqa: RUF012
    success_url = reverse_lazy("home")
    context_object_name = "article"

    # Add code to convert markdown to HTML
    md = markdown.Markdown(extensions=["fenced_code", "tables", "attr_list", "def_list", "nl2br"])

    def get_context_data(self, **kwargs):
        """Convert markdown in article.content to HTML."""
        md = markdown.Markdown(extensions=["fenced_code", "tables", "attr_list", "def_list", "nl2br"])
        context = super().get_context_data(**kwargs)
        html = md.convert(context["article"].content)
        context["markdown_html"] = html
        return context



class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an Article."""

    model = Article
    template_name = "app/article_update.html"
    fields = ["title", "content",  "twitter_post", "status"]  # noqa: RUF012
    success_url = reverse_lazy("authors")
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

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Override post to set the success message."""
        messages.success(self.request, "Article deleted successfully.", extra_tags="destructive")
        return super().post(request, *args, **kwargs)
