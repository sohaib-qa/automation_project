import pytest, re
import random
import string
from playwright.sync_api import Page, expect
from test_data import (

    START_DATE_FULL,
    START_DATE_DAY,
    END_DATE_FULL,
    END_DATE_DAY,
)
from conftest import assert_row_present


def rid(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


#
BRANCH_NAME = "test_branch_owhbpd"
LOCATION_NAME = f"Automation_{rid(4)}"
LOCATION_NAME1 = f"Automation_{rid(4)}"
LOCATION_NAME2 = f"Automation_{rid(4)}"
LOCATION_NAME3 = f"Automation_{rid(4)}"
LOCATION_NAME4 = f"Automation_{rid(4)}"


def test_create_location(page: Page):

    # # --- Navigate to Locations ---
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Locations']", state="visible")
    # page.wait_for_timeout(1500)
    #
    # page.locator("//span[normalize-space()='Locations']").click()
    page.goto("https://vyzor.app/#/locations")
    page.reload()
    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(1500)

    page.locator("#vz_datatable_create_button").click()

    # page.get_by_text("Add Location").click()
    page.wait_for_timeout(1500)

    page.locator("input[name='name']").fill(LOCATION_NAME)
    page.wait_for_timeout(1500)

    # --- Select Branch (dropdown) ---
    # --- Select Branch (dropdown) ---
    # branch_field = page.get_by_label("Branches *")
    # branch_field.locator("div.multiselect__select").click()
    #
    # # Wait for list to appear
    # page.wait_for_selector("li.multiselect__element span", timeout=8000)

    # Select the branch from dropdown using test_data.py value
    page.locator("//span[normalize-space()='Please select branch']").click()
    page.wait_for_timeout(2000)
    page.get_by_role("option", name=BRANCH_NAME).locator("span").first.click()

    # --- Select Start Date = today ---
    page.locator("input[name='startDate']").click()
    page.locator(f"[data-test*='{START_DATE_FULL}']").get_by_text(START_DATE_DAY).click()

    # --- Select End Date = today + 1 day ---
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{END_DATE_FULL}']").get_by_text(END_DATE_DAY).click()

    # ✅ Save (scoped to modal)
    page.locator("div[role='dialog']").get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")

    # ✅ Validate in table
    assert_row_present(page, LOCATION_NAME)


def test_create_location1(page: Page):
    # page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    # page.goto("https://vyzor.app/#/locations", wait_until="networkidle")
    page.reload()
    page.wait_for_timeout(2000)
    # # --- Navigate to Locations ---
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Locations']", state="visible")
    # page.wait_for_timeout(1500)
    #
    # page.locator("//span[normalize-space()='Locations']").click()
    # page.wait_for_load_state("networkidle")
    # page.wait_for_timeout(1500)

    page.locator("#vz_datatable_create_button").click()

    # page.get_by_text("Add Location").click()
    page.wait_for_timeout(1500)

    page.locator("input[name='name']").fill(LOCATION_NAME1)
    page.wait_for_timeout(1500)

    # --- Select Branch (dropdown) ---
    # --- Select Branch (dropdown) ---
    # branch_field = page.get_by_label("Branches *")
    # branch_field.locator("div.multiselect__select").click()
    #
    # # Wait for list to appear
    # page.wait_for_selector("li.multiselect__element span", timeout=8000)

    # Select the branch from dropdown using test_data.py value
    page.locator("//span[normalize-space()='Please select branch']").click()
    page.wait_for_timeout(2000)
    page.get_by_role("option", name=BRANCH_NAME).locator("span").first.click()

    # --- Select Start Date = today ---
    page.locator("input[name='startDate']").click()
    page.locator(f"[data-test*='{START_DATE_FULL}']").get_by_text(START_DATE_DAY).click()

    # --- Select End Date = today + 1 day ---
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{END_DATE_FULL}']").get_by_text(END_DATE_DAY).click()

    # ✅ Save (scoped to modal)
    page.locator("div[role='dialog']").get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")

    # ✅ Validate in table
    assert_row_present(page, LOCATION_NAME1)


def test_multi_delete_Location(page: Page):
    # page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    # page.goto("https://vyzor.app/#/locations", wait_until="networkidle")
    page.reload()
    page.wait_for_timeout(5000)
    page.wait_for_load_state("networkidle")
    page.get_by_role("row", name=LOCATION_NAME).get_by_role("checkbox").first.check()
    page.get_by_role("row", name=LOCATION_NAME1).get_by_role("checkbox").check()
    page.get_by_role("button", name="Delete Selected").click(button="left")
    page.locator("//button[normalize-space()='Delete']").click()


def test_create_location2(page: Page):
    # page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    # page.goto("https://vyzor.app/#/locations", wait_until="networkidle")
    page.reload()
    page.wait_for_timeout(2000)
    # --- Navigate to Locations ---
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Locations']", state="visible")
    # page.wait_for_timeout(1500)
    #
    # page.locator("//span[normalize-space()='Locations']").click()
    # page.wait_for_load_state("networkidle")
    # page.wait_for_timeout(1500)

    page.locator("#vz_datatable_create_button").click()

    # page.get_by_text("Add Location").click()
    page.wait_for_timeout(1500)

    page.locator("input[name='name']").fill(LOCATION_NAME2)
    page.wait_for_timeout(1500)

    # --- Select Branch (dropdown) ---
    # --- Select Branch (dropdown) ---
    # branch_field = page.get_by_label("Branches *")
    # branch_field.locator("div.multiselect__select").click()
    #
    # # Wait for list to appear
    # page.wait_for_selector("li.multiselect__element span", timeout=8000)

    # Select the branch from dropdown using test_data.py value
    page.locator("//span[normalize-space()='Please select branch']").click()
    page.wait_for_timeout(2000)
    page.get_by_role("option", name=BRANCH_NAME).locator("span").first.click()

    # --- Select Start Date = today ---
    page.locator("input[name='startDate']").click()
    page.locator(f"[data-test*='{START_DATE_FULL}']").get_by_text(START_DATE_DAY).click()

    # --- Select End Date = today + 1 day ---
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{END_DATE_FULL}']").get_by_text(END_DATE_DAY).click()

    # ✅ Save (scoped to modal)
    page.locator("div[role='dialog']").get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")

    # ✅ Validate in table
    assert_row_present(page, LOCATION_NAME2)


def test_search_Location(page: Page):
    # page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    # page.goto("https://vyzor.app/#/locations", wait_until="networkidle")
    page.reload()
    page.get_by_role("textbox", name="Search").first.click()
    page.get_by_role("textbox", name="Search").first.type(LOCATION_NAME2)
    page.get_by_role("textbox", name="Search").first.press("Enter")
    location_search = page.locator(f"//span[@class='text-truncate'][normalize-space()='{LOCATION_NAME2}']")
    expect(location_search).to_have_text(LOCATION_NAME2)


# def test_filter_Location(logged_in_page: Page):
#     page = logged_in_page
#     page.get_by_role("button", name=" Filter 1").click()
#     page.locator("#vz-filter-data-locations div").filter(has_text=re.compile(r"^Select option$")).click()
#     page.get_by_role("option", name="Dining Area").locator("span").first.click()
#
#     page.get_by_role("textbox", name="Start date").click()
#     page.locator(".available.today > .el-date-table-cell > .el-date-table-cell__text").first.click()
#     page.locator(".available.in-range.end-date > .el-date-table-cell > .el-date-table-cell__text").click()
#     page.get_by_role("button", name="OK").click()
#     page.get_by_role("button", name="Apply").click()
#     page.get_by_role("button", name=" Filter 3").click()
#     page.get_by_role("button", name="Reset").click()


def test_single_delete_Location(page: Page):
    # page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    # page.goto("https://vyzor.app/#/locations", wait_until="networkidle")
    page.reload()
    table = page.locator("table").first
    page.get_by_role("row", name=LOCATION_NAME2).locator("a").nth(1).click()
    page.get_by_role("button", name="Delete").click()
    # expect(LOCATION_NAME2).not_to_be_visible()
    expect(table.get_by_role("row", name=LOCATION_NAME2)).to_have_count(0)


# def test_activity_location_deleted(logged_in_page: Page):
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
#     expect(event_cell).to_contain_text("room1")
#     expect(event_cell).to_contain_text("deleted")

def test_create_location3(page: Page):
    # page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    # page.goto("https://vyzor.app/#/locations", wait_until="networkidle")
    page.reload()
    page.wait_for_timeout(2000)
    # --- Navigate to Locations ---
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Locations']", state="visible")
    # page.wait_for_timeout(1500)
    #
    # page.locator("//span[normalize-space()='Locations']").click()
    # page.wait_for_load_state("networkidle")
    # page.wait_for_timeout(1500)

    page.locator("#vz_datatable_create_button").click()

    # page.get_by_text("Add Location").click()
    page.wait_for_timeout(1500)

    page.locator("input[name='name']").fill(LOCATION_NAME3)
    page.wait_for_timeout(1500)

    # --- Select Branch (dropdown) ---
    # --- Select Branch (dropdown) ---
    # branch_field = page.get_by_label("Branches *")
    # branch_field.locator("div.multiselect__select").click()
    #
    # # Wait for list to appear
    # page.wait_for_selector("li.multiselect__element span", timeout=8000)

    # Select the branch from dropdown using test_data.py value
    page.locator("//span[normalize-space()='Please select branch']").click()
    page.wait_for_timeout(2000)
    page.get_by_role("option", name=BRANCH_NAME).locator("span").first.click()

    # --- Select Start Date = today ---
    page.locator("input[name='startDate']").click()
    page.locator(f"[data-test*='{START_DATE_FULL}']").get_by_text(START_DATE_DAY).click()

    # --- Select End Date = today + 1 day ---
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{END_DATE_FULL}']").get_by_text(END_DATE_DAY).click()

    # ✅ Save (scoped to modal)
    page.locator("div[role='dialog']").get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")

    # ✅ Validate in table
    assert_row_present(page, LOCATION_NAME3)


def test_edit_location(page: Page):
    page.get_by_role("row", name=LOCATION_NAME3).locator("a").first.click()
    page.locator("input[name='name']").fill(LOCATION_NAME4)
    page.locator("div[role='dialog']").get_by_role("button", name="Save").click()
    page.wait_for_timeout(1500)
    assert_row_present(page, LOCATION_NAME4)


def test_activity_location_updated(page: Page):
    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(2000)
    page.locator("#kt_lookup_drawer_toggle-activity").click()
    expect(page.locator("#kt_lookup_drawer")).to_be_visible()

    # Search activity
    search_box = page.locator("#kt_lookup_drawer").get_by_role(
        "textbox", name="Search"
    )
    search_box.fill(LOCATION_NAME4)
    search_box.press("Enter")

    update_messages = [
        "location name has been updated from",

    ]

    for message in update_messages:
        expect(
            page.locator(
                f'span[title*="{LOCATION_NAME4}"][title*="{message}"]'
            )
        ).to_be_visible()

