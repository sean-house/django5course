"""Models for the app."""
import re

from django.contrib.auth.models import AbstractUser
from django.db import models

ARTICLE_STATUS = (("draft", "draft"), ("inprogress", "in progress"), ("published", "published"))


# Create your models here.
class UserProfile(AbstractUser):
    """Model for a User profile."""

    pass  # noqa: PIE790


class Article(models.Model):
    """Model for the Article."""

    title = models.CharField(max_length=50)
    content = models.TextField(blank=True, default="")
    word_count = models.IntegerField(blank=True, default="")
    twitter_post = models.TextField(blank=True, default="")

    status = models.CharField(max_length=50, choices=ARTICLE_STATUS, default="draft")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        """Return a string representation of the Article."""
        return f"Article: {self.id}: Title: {self.title}"

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Override save method to update the word count field."""
        text = re.sub(r"<[^>]*>", "", self.content).replace("&nbsp;", " ")
        self.word_count = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)
