import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    # Ignore SSL errors
    return {"ignore_https_errors": True}


def test_valid_login(page):
    page.goto("https://vyzor.app/#/sign-in", wait_until="networkidle")

    # --- Valid Login ---
    page.wait_for_selector("input[name='username']", state="visible")
    page.locator("input[name='username']").fill("sohaib2@vyzor.com")

    page.wait_for_selector("input[type='password']", state="visible")
    page.locator("input[type='password']").fill("Password@355")

    page.wait_for_selector("button:has-text('Log in')")
    page.get_by_role("button", name="Log in").click()



    page.get_by_role("button", name="Log in").click()
    page.get_by_role("img", name="vyzor").click()
    page.get_by_text("Log Out").click()

    page.wait_for_timeout(2000)  # short pause after logout


def test_no_branch_access(page):
    page.goto("https://vyzor.app/#/sign-in", wait_until="networkidle")

    page.wait_for_selector("input[name='username']", state="visible")
    page.locator("input[name='username']").fill("Sohaib@vyzor.com")

    page.wait_for_selector("input[type='password']", state="visible")
    page.locator("input[type='password']").fill("Password@355")

    page.get_by_role("button", name="Log in").click()
    page.wait_for_load_state("networkidle")

    expect(page.get_by_text("You do not have access to any branch", exact=False)).to_be_visible(timeout=8000)

    page.wait_for_timeout(2000)


def test_invalid_email(page):
    page.goto("https://vyzor.app/#/sign-in", wait_until="networkidle")

    # --- Invalid Email Format ---
    page.wait_for_selector("input[name='username']", state="visible")
    page.locator("input[name='username']").fill("Sohaib@vyzor.comh")

    page.wait_for_selector("input[type='password']", state="visible")
    page.locator("input[type='password']").fill("Password@355")

    page.get_by_role("button", name="Log in").click()
    page.wait_for_load_state("networkidle")

    expect(page.get_by_text("Invalid email address")).to_be_visible(timeout=8000)
    page.wait_for_timeout(2000)


def test_invalid_credentials(page):
    page.goto("https://vyzor.app/#/sign-in", wait_until="networkidle")

    # --- Wrong Password ---
    page.wait_for_selector("input[name='username']", state="visible")
    page.locator("input[name='username']").fill("Sohaib2@vyzor.com")

    page.wait_for_selector("input[type='password']", state="visible")
    page.locator("input[type='password']").fill("WrongPassword@123")

    page.get_by_role("button", name="Log in").click()
    page.wait_for_load_state("networkidle")

    expect(page.get_by_text("Bad credentials")).to_be_visible(timeout=8000)
    page.wait_for_timeout(2000)
