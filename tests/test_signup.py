import re

from django.core import mail

from playwright.sync_api import Page
from allauth.account.models import EmailAddress

from tests.pages.auth import LoginPage, SignupPage, ConfirmationPage
from app.models import UserProfile

def test_signup(page: Page, user_data: dict):
    page.goto('/accounts/signup')
    signup_page = SignupPage(page)
    signup_page.fill(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        email=user_data["email"],
        password=user_data["password"],
    )

    confirmation_link = re.search(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        mail.outbox[0].body).group()
    
    page.goto(confirmation_link)
    confirmation_page = ConfirmationPage(page)
    confirmation_page.submit_button.click()

    user = UserProfile.objects.get(last_name=user_data["last_name"])

    email_address = EmailAddress.objects.get(user=user)
    assert email_address.email == user_data["email"].lower()  # Note email is lowercased when saved
    assert email_address.verified 
    