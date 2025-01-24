from playwright.sync_api import Page

def test_can_load_homepage(page: Page):
    page.goto('/')
    assert "Welcome to the Camberley Repair Cafe" in page.content()
    