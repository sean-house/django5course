import os

import pytest
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email

from playwright.sync_api import Page
from django.contrib.auth import get_user_model
from django.test import Client
from pytest_django.live_server_helper import LiveServer

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

@pytest.fixture
def browser_context_args(live_server: LiveServer):
    
    return {"base_url": live_server.url}

# @pytest.fixture
# def test_server(live_server: LiveServer):
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch()
#         browser_context = browser.new_context(base_url=live_server.url)
#         page = browser_context.new_page()
#         yield page
#         browser_context.close()
#         browser.close()

@pytest.fixture
def user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "5ml8y@example.com",
        "password": "test_password1234",
    }

@pytest.fixture
def verified_user(user_data):
    user = get_user_model().objects.create_user(**user_data)
    user.is_active = True

    email, created = EmailAddress.objects.get_or_create(user=user, email=user_data["email"])
    email.verified = True

    user.save()
    email.save()
    return user

@pytest.fixture
def auth_page(page: Page, verified_user, user_data):
    client = Client()
    resp = client.post("/accounts/login/", data={"login": user_data["email"], "password": user_data["password"]})

    session_id = resp.cookies["sessionid"].value
    page.context.add_cookies(
        [
            {"name": "sessionid",
             "value": session_id,
             "domain": "localhost",
             "path": "/",
             },
        ],
    )
    return page
