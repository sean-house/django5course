"""Models for the app."""
import re

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.managers import UserProfileManager

ARTICLE_STATUS = (("draft", "draft"), ("inprogress", "in progress"), ("published", "published"))


# Create your models here.
class UserProfile(AbstractUser):
    """Model for a User profile."""

    email = models.EmailField(_("email address"), unique=True, max_length=254)

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]  # noqa: RUF012

    @property
    def article_count(self):  # noqa: ANN201
        """Return the number of articles created by the user."""
        return self.articles.count()

    @property
    def written_words(self):  # noqa: ANN201
        """Return the total number of words written by the user."""
        return self.articles.aggregate(models.Sum("word_count"))["word_count__sum"] or 0




class Article(models.Model):
    """Model for the Article."""

    class Meta:
        """Meta class for the Article model."""

        verbose_name = _("article")
        verbose_name_plural = _("articles")

    title = models.CharField(verbose_name=_("title"),  # noqa: DJ012
                             max_length=50)
    content = models.TextField(verbose_name=_("content"),
                               blank=True, default="")
    word_count = models.IntegerField(verbose_name=_("word count"),
                                     blank=True, default="")
    twitter_post = models.TextField(verbose_name=_("twitter post"),
                                    blank=True, default="")
    status = models.CharField(verbose_name=_("status"),
                              max_length=50, choices=ARTICLE_STATUS, default="draft")
    created_at = models.DateField(verbose_name=_("created at"),
                                  auto_now_add=True)
    updated_at = models.DateField(verbose_name=_("updated at"),
                                  auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="articles",
                                verbose_name=_("creator"))

    def __str__(self) -> str:
        """Return a string representation of the Article."""
        return f"Article: {self.id}: Title: {self.title}"

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Override save method to update the word count field."""
        text = re.sub(r"<[^>]*>", "", self.content).replace("&nbsp;", " ")
        self.word_count = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)
