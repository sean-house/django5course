import pytest

from playwright.sync_api import Page

from app.models import Article

from tests.pages.articles import ArticlesPage, ArticlePage

# Create some articles to enable testing of search
@pytest.fixture
def created_articles(verified_user):
    Article.objects.create(
        title="Test article 1",
        content="Test content 1",
        status="published",
        creator=verified_user,
    )
    Article.objects.create(
        title="Test article 2",
        content="Test content 2",
        status="draft",
        creator=verified_user,
    )


def test_empty_articles_page(auth_page: Page):
    auth_page.goto('/articles/authors/')
    authors_page = ArticlesPage(auth_page)
    assert authors_page.welcome_heading.is_visible()
    assert authors_page.no_articles_message.is_visible()

def test_search_articles(auth_page: Page, created_articles):
    auth_page.goto('/articles/authors/')
    authors_page = ArticlesPage(auth_page)
    authors_page.search_input.fill("2")
    authors_page.search_button.click()
    assert authors_page.page.get_by_text("Test article 2", exact=True).is_visible()
    assert authors_page.page.get_by_text("Test article 1", exact=True).is_hidden()

def test_search_and_clear(auth_page: Page, created_articles):
    auth_page.goto('/articles/authors/')
    authors_page = ArticlesPage(auth_page)
    authors_page.search_input.fill("2")
    authors_page.search_button.click()
    authors_page.clear_search_button.click()
    assert authors_page.page.get_by_text("Test article 2", exact=True).is_visible()
    assert authors_page.page.get_by_text("Test article 1", exact=True).is_visible()

def test_create_article(auth_page: Page):
    auth_page.goto('/articles/create/')
    article_page = ArticlePage(auth_page)
    article_page.fill_article("Test article 1", "Test content 1", "published", "Test twitter post 1")
    article_page.save_button.click()

    articles_page = ArticlesPage(auth_page)
    assert articles_page.page.get_by_text("Test article 1", exact=True).is_visible()

def test_create_edit_article(auth_page: Page):
    auth_page.goto('/articles/create/')
    article_page = ArticlePage(auth_page)
    article_page.fill_article("Test article 1", "Test content 1", "published", "Test twitter post 1")
    article_page.save_button.click()

    articles_page = ArticlesPage(auth_page)
    articles_page.page.get_by_text("Test article 1", exact=True).click()  # From the list click on the article created

    article_page = ArticlePage(auth_page)

    assert (
        "Test content 1"
        in article_page.content_editor.text_content()
        )