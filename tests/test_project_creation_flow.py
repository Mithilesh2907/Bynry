import os
import uuid
import requests
from playwright.sync_api import Page, expect


BASE_URL = os.getenv("BASE_URL", "https://app.workflowpro.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://app.workflowpro.com/api/v1")
TOKEN = os.getenv("TOKEN", "sample_token")

EMAIL = os.getenv("EMAIL", "admin@company1.com")
PASSWORD = os.getenv("PASSWORD", "password123")

TENANT2_EMAIL = os.getenv("TENANT2_EMAIL", "admin@company2.com")
TENANT2_PASSWORD = os.getenv("TENANT2_PASSWORD", "password123")


def login(page: Page, email: str, password: str):
    page.goto(f"{BASE_URL}/login")

    page.fill("#email", email)
    page.fill("#password", password)

    with page.expect_navigation():
        page.click("#login-btn")


def logout(page: Page):
    page.click("#profile-menu")
    page.click("#logout-btn")


def test_project_creation_flow(page: Page):
    """
    End-to-end workflow:
    1. Create project via API
    2. Verify project in UI
    3. Verify tenant isolation
    4. Delete project
    """

    project_name = f"Automation_Project_{uuid.uuid4().hex[:8]}"

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    # Step 1 - Create project using API
    response = requests.post(
        f"{API_BASE_URL}/projects",
        headers=headers,
        json={
            "name": project_name,
            "description": "Created by automation"
        }
    )

    assert response.status_code == 201

    project_id = response.json().get("id")

    try:

        # Step 2 - Verify in Web UI
        login(page, EMAIL, PASSWORD)

        expect(
            page.locator(f"text={project_name}")
        ).to_be_visible(timeout=15000)

        logout(page)

        # Step 3 - Verify tenant isolation
        login(page, TENANT2_EMAIL, TENANT2_PASSWORD)

        expect(
            page.locator(f"text={project_name}")
        ).not_to_be_visible()

    finally:

        # Step 4 - Cleanup
        requests.delete(
            f"{API_BASE_URL}/projects/{project_id}",
            headers=headers
        )