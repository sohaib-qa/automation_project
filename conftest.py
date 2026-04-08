# tests/conftest.py
import os
import pytest
from playwright.sync_api import Playwright
from test_data import ADMIN_EMAIL, ADMIN_PASSWORD


# ───────────────────────────────────────────────
# 1) Headless option
# ───────────────────────────────────────────────
def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False,
                     help="Run browser in headless mode")


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):
    return {"headless": pytestconfig.getoption("--headless")}


# ───────────────────────────────────────────────
# 2) SINGLE browser + SINGLE context for all tests
# ───────────────────────────────────────────────
@pytest.fixture(scope="session")
def context(playwright: Playwright, browser_type_launch_args):
    """Launch browser ONCE per test session."""
    browser = playwright.chromium.launch(**browser_type_launch_args, slow_mo=100)
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={"width": 1600, "height": 900},
        java_script_enabled=True,
    )
    yield context
    browser.close()   # Close only AFTER all tests finish


@pytest.fixture(scope="session")
def page(context):
    """Single shared page across all tests (session stays alive)."""
    page = context.new_page()
    yield page
    # Do NOT close page (keeps login session alive)


# ───────────────────────────────────────────────
# 3) Login ONCE for all tests
# ───────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def login_once(page):
    """Login only once and keep session alive."""
    page.goto("https://vyzor.app/#/sign-in", wait_until="networkidle")
    page.wait_for_selector("//input[@name='username']", timeout=20000)
    page.fill("//input[@name='username']", ADMIN_EMAIL)
    page.fill("input[type='password']", ADMIN_PASSWORD)
    page.get_by_role("button", name="Log in").click()
    page.wait_for_load_state("networkidle")
    print("✔ Logged in once for all tests")
    return page


# ───────────────────────────────────────────────
# 4) After each test → refresh URL but do NOT log out
# ───────────────────────────────────────────────
@pytest.fixture()
def logged_in_page(page):
    """Gives a fresh page but same login session."""
    page.reload()
    return page


# ───────────────────────────────────────────────
# 5) Screenshot on failure
# ───────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    extra = getattr(item, "extra", [])
    if extra:
        rep.extra = extra
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(page, request):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        os.makedirs("screenshots", exist_ok=True)
        path = os.path.join("screenshots", f"{request.node.name}.png")
        page.screenshot(path=path, full_page=True)
        print(f"\n📸 Screenshot saved: {path}")


# ───────────────────────────────────────────────
# 6) Helper: row check
# ───────────────────────────────────────────────
def assert_row_present(page, text, retries=5, pause_ms=2000):
    page.wait_for_selector("//table//tbody//tr", timeout=30000)
    locator = page.locator("//table//tbody//tr").filter(has_text=text)

    for i in range(retries):
        if locator.count() > 0:
            print(f"✔ Found row: {text}")
            return
        page.wait_for_timeout(pause_ms)

    raise AssertionError(f"Row not found: {text}")
