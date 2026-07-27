import os
from playwright.sync_api import Page, expect


BASE_URL = os.getenv("BASE_URL", "https://app.workflowpro.com")

TENANT1_EMAIL = os.getenv("TENANT1_EMAIL", "admin@company1.com")
TENANT1_PASSWORD = os.getenv("TENANT1_PASSWORD", "password123")

TENANT2_EMAIL = os.getenv("TENANT2_EMAIL", "admin@company2.com")
TENANT2_PASSWORD = os.getenv("TENANT2_PASSWORD", "password123")

PROJECT_NAME = "Automation_Project_1234"


def login(page: Page, email: str, password: str):
    """Helper function to perform login."""

    page.goto(f"{BASE_URL}/login")

    page.fill("#email", email)
    page.fill("#password", password)

    with page.expect_navigation():
        page.click("#login-btn")


def logout(page: Page):
    """Helper function to perform logout."""

    page.click("#profile-menu")
    page.click("#logout-btn")


def test_tenant_isolation(page: Page):
    """
    Verify that projects belonging to one tenant
    are not visible to another tenant.
    """

    # Login as Tenant 1
    login(page, TENANT1_EMAIL, TENANT1_PASSWORD)

    expect(
        page.locator(f"text={PROJECT_NAME}")
    ).to_be_visible()

    logout(page)

    # Login as Tenant 2
    login(page, TENANT2_EMAIL, TENANT2_PASSWORD)

    expect(
        page.locator(f"text={PROJECT_NAME}")
    ).not_to_be_visible()