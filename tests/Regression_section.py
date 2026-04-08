import re
import random
import string
from playwright.sync_api import Page, expect
from test_data import (
    TODAY_FULL,
    TODAY_DAY

)
from conftest import assert_row_present


def rid(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


SECTION_NAME = f"Automation_{rid()}"
SECTION_NAME2 = f"Automation_{rid()}"
SECTION_NAME3 = f"Automation_{rid()}"
SECTION_NAME4 = f"Automation_{rid()}"
clone = f"auto_clone_{rid()}"


def test_create_section_edit(page: Page):
    page.goto("https://vyzor.app/#/sections")
    page.wait_for_load_state("networkidle")

    # page.locator("#TemplatesTemplates").click()
    # page.get_by_role("link", name=" Sections").click()
    page.get_by_text("Add Section").click()
    page.locator("input[name=\"name\"]").click()
    page.locator("input[name=\"name\"]").fill(SECTION_NAME)
    page.locator("input[name=\"startDate\"]").click()
    page.wait_for_timeout(1000)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.locator("input[name=\"endDate\"]").click()
    page.wait_for_timeout(1000)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.get_by_role("button", name="Save").click()

    # edit section
    page.get_by_role("row", name=re.compile(f"{SECTION_NAME}.*{TODAY_DAY}")).get_by_role("link").click()

    page.locator("div").filter(has_text=re.compile(r"^Rows$")).get_by_role("spinbutton").click()
    page.locator("div").filter(has_text=re.compile(r"^Rows$")).get_by_role("spinbutton").fill("4")
    page.locator("div").filter(has_text=re.compile(r"^Columns\(Max 6\)$")).get_by_role("spinbutton").click()
    page.locator("div").filter(has_text=re.compile(r"^Columns\(Max 6\)$")).get_by_role("spinbutton").fill("3")
    page.get_by_role("button", name="Confirm").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.locator("p").first.click()
    # page.locator("p").first.click()
    # page.get_by_text("Attachements").click()
    # page.locator("[id=\"33760f13-1af7-4b11-a2cf-ff7b474f60df\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Bar Code", exact=True).click()
    # page.locator("[id=\"304effa5-6a88-4c6d-b246-9859f0d4d98e\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Bar Code Validator").click()
    # page.locator("[id=\"36a28b8b-cbd1-4c8a-9575-dcf8f9e1e9ca\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Camera").click()
    page.get_by_role("button", name="Publish").dblclick()
    page.locator("#kt_chat_messenger_header").get_by_role("link").click()
    assert_row_present(page, SECTION_NAME)


#
def test_edit_section(page: Page):
    page.get_by_role("row", name=SECTION_NAME).locator("a").nth(1).click()
    page.locator("input[name=\"name\"]").click()
    page.locator("input[name=\"name\"]").fill(SECTION_NAME2)
    page.get_by_role("button", name="Save").click()


def test_activity_Section_updated(page: Page):
    page.locator("#kt_lookup_drawer_toggle-activity").click()
    drawer = page.locator("#kt_lookup_drawer")
    expect(drawer).to_be_visible()

    # Search activity
    search_box = drawer.get_by_role("textbox", name="Search")
    search_box.fill(SECTION_NAME2)
    search_box.press("Enter")

    update_messages = [
        "section name has been updated from",
    ]

    for message in update_messages:
        expect(
            page.locator(
                f'span[title*="{SECTION_NAME2}"][title*="{message}"]'
            )
        ).to_be_visible()


def test_create_section_edit1(page: Page):
    page.reload()
    page.get_by_text("Add Section").click()
    page.locator("input[name=\"name\"]").click()
    page.locator("input[name=\"name\"]").fill(SECTION_NAME3)
    page.locator("input[name=\"startDate\"]").click()
    page.wait_for_timeout(1000)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.locator("input[name=\"endDate\"]").click()
    page.wait_for_timeout(1000)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.get_by_role("button", name="Save").click()

    # edit section
    page.get_by_role("row", name=re.compile(f"{SECTION_NAME3}.*{TODAY_DAY}")).get_by_role("link").click()

    page.locator("div").filter(has_text=re.compile(r"^Rows$")).get_by_role("spinbutton").click()
    page.locator("div").filter(has_text=re.compile(r"^Rows$")).get_by_role("spinbutton").fill("4")
    page.locator("div").filter(has_text=re.compile(r"^Columns\(Max 6\)$")).get_by_role("spinbutton").click()
    page.locator("div").filter(has_text=re.compile(r"^Columns\(Max 6\)$")).get_by_role("spinbutton").fill("3")
    page.get_by_role("button", name="Confirm").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.locator("p").first.click()
    # page.locator("p").first.click()
    # page.get_by_text("Attachements").click()
    # page.locator("[id=\"33760f13-1af7-4b11-a2cf-ff7b474f60df\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Bar Code", exact=True).click()
    # page.locator("[id=\"304effa5-6a88-4c6d-b246-9859f0d4d98e\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Bar Code Validator").click()
    # page.locator("[id=\"36a28b8b-cbd1-4c8a-9575-dcf8f9e1e9ca\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Camera").click()
    page.get_by_role("button", name="Publish").dblclick()
    page.locator("#kt_chat_messenger_header").get_by_role("link").click()
    assert_row_present(page, SECTION_NAME3)


def test_multi_delete_Section(page: Page):
    page.reload()

    page.wait_for_load_state("networkidle")
    table = page.locator("table").first
    page.get_by_role("row", name=SECTION_NAME2).get_by_role("checkbox").check()
    page.get_by_role("row", name=SECTION_NAME3).get_by_role("checkbox").check()
    page.get_by_role("button", name="Delete Selected").click(button="left")
    page.locator("//button[normalize-space()='Delete']").click()
    expect(table.get_by_role("row", name=SECTION_NAME2)).to_have_count(0)
    expect(table.get_by_role("row", name=SECTION_NAME3)).to_have_count(0)


def test_create_section_edit2(page: Page):
    page.reload()
    page.get_by_text("Add Section").click()
    page.locator("input[name=\"name\"]").click()
    page.locator("input[name=\"name\"]").fill(SECTION_NAME4)
    page.locator("input[name=\"startDate\"]").click()
    page.wait_for_timeout(1000)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.locator("input[name=\"endDate\"]").click()
    page.wait_for_timeout(1000)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.get_by_role("button", name="Save").click()

    # edit section
    page.get_by_role("row", name=re.compile(f"{SECTION_NAME4}.*{TODAY_DAY}")).get_by_role("link").click()

    page.locator("div").filter(has_text=re.compile(r"^Rows$")).get_by_role("spinbutton").click()
    page.locator("div").filter(has_text=re.compile(r"^Rows$")).get_by_role("spinbutton").fill("4")
    page.locator("div").filter(has_text=re.compile(r"^Columns\(Max 6\)$")).get_by_role("spinbutton").click()
    page.locator("div").filter(has_text=re.compile(r"^Columns\(Max 6\)$")).get_by_role("spinbutton").fill("3")
    page.get_by_role("button", name="Confirm").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.get_by_text("Attachements").click()
    # page.locator("p").first.click()
    # page.locator("p").first.click()
    # page.get_by_text("Attachements").click()
    # page.locator("[id=\"33760f13-1af7-4b11-a2cf-ff7b474f60df\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Bar Code", exact=True).click()
    # page.locator("[id=\"304effa5-6a88-4c6d-b246-9859f0d4d98e\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Bar Code Validator").click()
    # page.locator("[id=\"36a28b8b-cbd1-4c8a-9575-dcf8f9e1e9ca\"] > .d-flex > .col-md-12 > p").click()
    # page.get_by_text("Camera").click()
    page.get_by_role("button", name="Publish").dblclick()
    page.locator("#kt_chat_messenger_header").get_by_role("link").click()
    assert_row_present(page, SECTION_NAME4)


def test_search_Section(page: Page):
    page.reload()
    page.get_by_role("textbox", name="Search").first.click()
    page.get_by_role("textbox", name="Search").first.type(SECTION_NAME4)
    page.get_by_role("textbox", name="Search").first.press("Enter")
    form_search = page.locator(f"//span[@class ='text-truncate'][normalize-space()='{SECTION_NAME4}']")
    expect(form_search).to_contain_text(SECTION_NAME4)


def test_single_delete_Section(page: Page):
    table = page.locator("table").first
    page.get_by_role("gridcell", name=SECTION_NAME4).locator("a").nth(1).click()
    # page.get_by_role("row", name=SECTION_NAME4).locator("a").click()
    page.get_by_role("button", name="Delete").click()
    expect(table.get_by_role("row", name=SECTION_NAME4)).to_have_count(0)

# def test_activity_Section_deleted(logged_in_page: Page):
#     page = logged_in_page
#
#     # Open activity drawer
#     page.locator("#kt_lookup_drawer_toggle-activity").click()
#     expect(page.locator("#kt_lookup_drawer")).to_be_visible()
#
#     # Search activity
#     search_box = page.locator("#kt_lookup_drawer").get_by_role(
#         "textbox", name="Search"
#     )
#     search_box.fill("room1")
#     search_box.press("Enter")
#
#     # Get latest activity row (skip header)
#     latest_row = (
#         page.locator("#kt_lookup_drawer")
#         .get_by_role("row")
#         .nth(1)
#     )
#
#     # Event column
#     event_cell = latest_row.locator(".text-truncate").nth(2)
#
#     # Assertions
#     expect(event_cell).to_contain_text("section")
#     expect(event_cell).to_contain_text("deleted")


# def test_filter_Section(logged_in_page: Page):
#     page = logged_in_page
#     page.get_by_role("button", name=" Filter 1").click()
#     page.locator("#vz-filter-data-forms div").filter(has_text=re.compile(r"^Select option$")).click()
#     page.locator("#vz-filter-data-forms span").filter(has_text="auto section").first.click()
#     page.get_by_role("textbox", name="Start date").click()
#     page.locator(".available > .el-date-table-cell > .el-date-table-cell__text").first.click()
#     page.locator(".available.in-range.end-date > .el-date-table-cell > .el-date-table-cell__text").click()
#     page.get_by_role("button", name="OK").click()
#     page.get_by_role("button", name="Apply").click()
#     page.get_by_role("button", name=" Filter 3").click()
#     page.get_by_role("button", name="Reset").click()
