import os
from playwright.sync_api import Page, expect


BASE_URL = os.getenv("BASE_URL", "https://app.workflowpro.com")
EMAIL = os.getenv("EMAIL", "admin@company1.com")
PASSWORD = os.getenv("PASSWORD", "password123")


def test_successful_login(page: Page):
    """
    Verify that a valid user can successfully log in
    and is redirected to the dashboard.
    """

    page.goto(f"{BASE_URL}/login")

    page.fill("#email", EMAIL)
    page.fill("#password", PASSWORD)

    with page.expect_navigation():
        page.click("#login-btn")

    expect(page).to_have_url(f"{BASE_URL}/dashboard")

    expect(
        page.locator("h1")
    ).to_contain_text("Dashboard")