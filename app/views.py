"""Views for the app."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from app.models import Article


# Create your views here.
class ArticleListView(ListView):
    """View for the list of Articles."""

    model = Article
    template_name = "app/home.html"
    context_object_name = "articles"


class ArticleCreateView(CreateView):
    """View for creating an Article."""

    model = Article
    template_name = "app/article_create.html"
    fields = ["title", "content", "twitter_post", "status"]  # noqa: RUF012
    success_url = reverse_lazy("home")


class ArticleUpdateView(UpdateView):
    """View for updating an Article."""

    model = Article
    template_name = "app/article_update.html"
    fields = ["title", "content",  "twitter_post", "status"]  # noqa: RUF012
    success_url = reverse_lazy("home")
    context_object_name = "article"


class ArticleDeleteView(DeleteView):
    """View for deleting an Article."""

    model = Article
    template_name = "app/article_delete.html"
    success_url = reverse_lazy("home")
    context_object_name = "article"
