from playwright.sync_api import Page

class SignupPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_field = page.get_by_placeholder("First name")
        self.last_name_field = page.get_by_placeholder("Last name")
        self.email_field = page.get_by_placeholder("Email address")
        self.password_field = page.get_by_placeholder("Password", exact=True)
        self.password_confirmation_field = page.get_by_placeholder("Password (again)", exact=True)
        self.submit_button = page.get_by_role("button", name="Create your account")

    def fill(self, first_name, last_name, email, password):
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.email_field.fill(email)
        self.password_field.fill(password)
        self.password_confirmation_field.fill(password)
        self.submit_button.click()

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_field = page.get_by_placeholder("Email address")
        self.password_field = page.get_by_placeholder("Password")
        self.submit_button = page.get_by_role("button", name="Sign in")

class ConfirmationPage:
    def __init__(self, page: Page):
        self.page = page
        self.submit_button = page.get_by_role("button")