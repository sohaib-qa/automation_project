# tests/test_create_branch.py
import string
import re
import random
from playwright.sync_api import Page,expect
def rid(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))
ROLE_NAME = f"auto_{rid()}"
ROLE_NAME1 = f"LK{rid()}"



def test_create_role(page: Page):

    page.locator("#UsersUsers").click()
    page.get_by_role("link", name=" Roles").click()
    page.get_by_text("Add Role").click()
    page.locator("#roleName").click()
    page.locator("#roleName").fill(ROLE_NAME)
    page.get_by_role("button", name="Save").click()

def test_role_filter(page: Page):
    page.get_by_role("button", name="", exact=True).click()
    page.locator("#vz-filter-data-roleFilters div").filter(has_text=re.compile(r"^Select option$")).click()
    page.get_by_role("textbox", name="Select option").type(ROLE_NAME)
    page.locator("#vz-filter-data-roleFilters").get_by_text(ROLE_NAME).click()
    page.get_by_role("button", name="Apply").click()
    page.get_by_role("button", name=" 1").click()
    page.get_by_role("button", name="Reset").click()

def test_role_search(page: Page):
    page.reload()
    page.wait_for_load_state("networkidle")
    page.locator("#kt_post input[name=\"search\"]").click()
    page.locator("#kt_post input[name=\"search\"]").fill(ROLE_NAME)
    page.locator("#kt_post input[name=\"search\"]").press("Enter")
    role_search=page.get_by_role("button", name=ROLE_NAME)
    expect(role_search).to_have_text(ROLE_NAME)


def test_role_delete(page: Page):
    page.wait_for_load_state("networkidle")
    page.locator("div.pointer-cursor", has_text=ROLE_NAME).locator("input[type='checkbox']").check()
    page.get_by_role("button", name=" Delete").click()
    page.get_by_role("button", name="Delete", exact=True).click()
        # page.locator("div.hoverClass", has_text=ROLE_NAME).locator("input[type='checkbox']").check()
        # # page.locator("div.hoverClass", has_text="Automation_nebg").locator("input[type='checkbox']").check()
        # page.get_by_role("button", name=" Delete").click()
        # page.get_by_role("button", name="Delete", exact=True).click()






