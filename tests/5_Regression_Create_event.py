import re
import random
import string
from playwright.sync_api import Page, expect

from conftest import assert_row_present


def rid(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


EVENT_NAME = f"{rid()}"
EVENT_NAME1 = f"{rid()}"
EVENT_NAME2 = f"{rid()}"
EVENT_NAME3 = f"{rid()}"
EVENT_NAME4 = f"{rid()}"
EVENT_NAME5 = f"{rid()}"
EMAIL = f"{rid()}@vyzor.com"
EMAIL1 = f"{rid()}@vyzor.com"
EMAIL2 = f"{rid()}@vyzor.com"
EMAIL3 = f"{rid()}@vyzor.com"
BRANCH_NAME = "test_branch_owhbpd"


def test_create_event(logged_in_page: Page):
    page = logged_in_page
    page.wait_for_load_state("networkidle")

    page.locator("#SettingsSettings").click()
    page.get_by_role("link", name=" Events").click()
    page.get_by_text("Add Event").click()
    page.wait_for_timeout(2000)
    page.locator("//input[@name='eventName']").fill(EVENT_NAME)
    page.get_by_role("textbox", name="Select Type").click()
    page.wait_for_timeout(2000)
    page.get_by_role("listitem").filter(has_text=re.compile(r"^Event$")).click()
    page.get_by_role("textbox", name="Select Sub Type").click()
    page.wait_for_timeout(1500)

    page.wait_for_selector(
        "//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space()='Scheduled Event']", timeout=10000)
    page.locator("//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space()='Scheduled Event']").click()

    page.get_by_role("textbox", name="Provider").click()
    page.get_by_role("listitem").filter(has_text="Vyzor Email Provider").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Save").click()
    # ---------------------
    assert_row_present(page, EVENT_NAME)


def test_edit_event(page: Page):
    page.get_by_role("row", name=EVENT_NAME).locator("a").first.click()
    page.get_by_role("textbox", name="Select Sub Type").click()
    page.get_by_role("listitem").filter(has_text="Event Form").click()
    page.get_by_role("button", name="Continue").click()
    page.locator("div").filter(has_text=re.compile(r"^Please select recipient$")).click()
    page.get_by_role("option", name="sohaib ahmad (sohaib2@vyzor.").locator("span").first.click()
    page.get_by_role("button", name="Continue").click()

    page.get_by_role("textbox", name="End Date").click()
    page.locator("#kt_modal_create_event").get_by_role("rowgroup").get_by_text("28").nth(1).click()
    page.get_by_role("button", name="OK").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Save").click()


def test_activity_event_updated(page: Page):
    page.locator("#kt_lookup_drawer_toggle-activity").click()
    drawer = page.locator("#kt_lookup_drawer")
    expect(drawer).to_be_visible()

    # Search activity
    search_box = drawer.get_by_role("textbox", name="Search")
    search_box.fill(EVENT_NAME)
    search_box.press("Enter")

    update_messages = [
        "event subject has been updated from",
        "event start date has been updated from",

    ]

    for message in update_messages:
        expect(
            page.locator(
                f'span[title*="{EVENT_NAME}"][title*="{message}"]'
            )
        ).to_be_visible()


def test_create_event1(page: Page):
    page.reload()

    page.wait_for_load_state("networkidle")
    #
    # page.locator("#SettingsSettings").click()
    # page.get_by_role("link", name=" Events").click()
    page.get_by_text("Add Event").click()
    page.wait_for_timeout(2000)
    page.locator("//input[@name='eventName']").fill(EVENT_NAME1)
    page.get_by_role("textbox", name="Select Type").click()
    page.wait_for_timeout(2000)
    page.get_by_role("listitem").filter(has_text=re.compile(r"^Event$")).click()
    page.get_by_role("textbox", name="Select Sub Type").click()
    page.wait_for_timeout(1500)

    page.wait_for_selector(
        "//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space()='Scheduled Event']",
        timeout=10000)
    page.locator(
        "//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space()='Scheduled Event']").click()

    page.get_by_role("textbox", name="Provider").click()
    page.get_by_role("listitem").filter(has_text="Vyzor Email Provider").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Save").click()
    # ---------------------
    assert_row_present(page, EVENT_NAME1)


def test_multi_delete_event(page: Page):
    page.reload()

    page.wait_for_timeout(5000)
    page.wait_for_load_state("networkidle")
    table = page.locator("table").first
    page.get_by_role("row", name=EVENT_NAME).get_by_role("checkbox").check()
    page.get_by_role("row", name=EVENT_NAME1).get_by_role("checkbox").check()
    page.get_by_role("button", name="Delete Selected").click(button="left")
    page.locator("//button[normalize-space()='Delete']").click()
    expect(table.get_by_role("row", name=EVENT_NAME)).to_have_count(0)
    expect(table.get_by_role("row", name=EVENT_NAME1)).to_have_count(0)


def test_create_event2(page: Page):
    page.reload()

    page.wait_for_load_state("networkidle")

    # page.locator("#SettingsSettings").click()
    # page.get_by_role("link", name=" Events").click()
    page.get_by_text("Add Event").click()
    page.wait_for_timeout(2000)
    page.locator("//input[@name='eventName']").fill(EVENT_NAME2)
    page.get_by_role("textbox", name="Select Type").click()
    page.wait_for_timeout(2000)
    page.get_by_role("listitem").filter(has_text=re.compile(r"^Event$")).click()
    page.get_by_role("textbox", name="Select Sub Type").click()
    page.wait_for_timeout(1500)

    page.wait_for_selector(
        "//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space()='Scheduled Event']",
        timeout=10000)
    page.locator(
        "//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space()='Scheduled Event']").click()

    page.get_by_role("textbox", name="Provider").click()
    page.get_by_role("listitem").filter(has_text="Vyzor Email Provider").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Save").click()
    # ---------------------
    assert_row_present(page, EVENT_NAME2)


def test_search_event(page: Page):
    page.reload()
    page.get_by_role("textbox", name="Search").first.click()
    page.get_by_role("textbox", name="Search").first.type(EVENT_NAME2)
    page.get_by_role("textbox", name="Search").first.press("Enter")
    event_search = page.page.get_by_role("row", name=EVENT_NAME2)
    expect(event_search).to_have_text(EVENT_NAME2)


def test_single_delete_user(page: Page):
    page.wait_for_timeout(2000)
    table = page.locator("table").first
    page.get_by_role("row", name=EVENT_NAME2).locator("a").nth(1).click()
    page.get_by_role("button", name="Delete").click()
    expect(table.get_by_role("row", name=EVENT_NAME2)).to_have_count(0)
