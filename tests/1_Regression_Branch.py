

import re
import random
import string
from datetime import datetime

from playwright.sync_api import Page, expect
from test_data import (
    BRANCH_NAME,
    BRANCH_CODE,
    TODAY_FULL,
    TODAY_DAY, BRANCH_NAME1, BRANCH_CODE1
)
from conftest import assert_row_present


def rid(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


BRANCH_NAME2 = f"test_branch_{rid()}"
BRANCH_NAME3 = f"test_branch_{rid()}"
BRANCH_NAME4 = f"test_branch_{rid()}"
clone = f"auto_clone_{rid()}"

BRANCH_CODE2 = str(random.randint(10000, 99999))
BRANCH_CODE3 = str(random.randint(10000, 99999))
BRANCH_CODE4 = str(random.randint(10000, 99999))
BRANCH_CODE5 = str(random.randint(10000, 99999))


def assert_field_value(page, label, expected_value):
    value_cell = page.locator(f"th:has-text('{label}') + td")
    expect(value_cell).to_contain_text(expected_value)


def test_create_and_verify_branch(logged_in_page: Page):
    page = logged_in_page

    # --- Open Business → Branches ---
    page.wait_for_selector("#BusinessBusiness", state="visible")
    page.locator("#BusinessBusiness").click()
    page.wait_for_selector("//span[normalize-space()='Branches']", state="visible")
    page.locator("//span[normalize-space()='Branches']").click()
    page.wait_for_load_state("networkidle")

    # --- Add Branch ---
    page.get_by_text("Add Branch").click()

    # Fill basic fields
    page.locator("input[name='name']").fill(BRANCH_NAME)
    page.locator("input[name='code']").fill(BRANCH_CODE)

    # Branch Level
    page.locator("//input[@placeholder='Please select branch level']").click()
    page.get_by_role("listitem").filter(has_text="Level 1").click()

    # Email + Website
    page.locator("//input[@placeholder='Email@example.com']").fill("test@gmail.com")
    page.locator("input[name='website']").fill("web.com")

    # --- Address Modal ---
    page.locator("#vz_add_edit_modal_scroll span").nth(3).click()  # Address button

    page.locator("#street").fill("line1")
    page.locator("#street2").fill("line2")

    page.get_by_role("textbox", name="Please select country").click()
    page.get_by_role("listitem").filter(has_text="Canada").click()

    page.locator("div").filter(has_text=re.compile(r"^State/Province/Region$")).get_by_role("img").click()
    page.get_by_role("listitem").filter(has_text="Manitoba").click()

    page.locator("#kt_modal_assign_user_scroll div").filter(has_text=re.compile(r"^City$")).get_by_role("img").click()
    page.wait_for_selector("//input[@placeholder='Please select city']", state="visible").click()
    page.get_by_role("listitem").filter(has_text="Altona").click()

    page.locator("#postalCode").fill("44000")

    # Save Address
    page.get_by_text("SavePlease wait...").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox", name="Please select time zone").click()
    page.get_by_text("(GMT-12:00) GMT+12, Etc").click()

    # --- End Date ---
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()

    # Description
    page.get_by_role("textbox", name="Description").fill("description test text")

    # Save branch
    page.get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")

    # --- Verify table row ---
    assert_row_present(page, BRANCH_NAME)


def test_verify_branch_details(page):
    # Assuming branch already created and detail page opened
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Branches']", state="visible")
    # page.locator("//span[normalize-space()='Branches']").click()
    page.reload()
    page.wait_for_load_state("networkidle")
    page.get_by_title(BRANCH_NAME, exact=True).locator("span").click()
    assert_field_value(page, "Branch Number:", BRANCH_CODE)
    assert_field_value(page, "Branch Level:", "Level 1")
    assert_field_value(page, "Email:", "test@gmail.com")
    assert_field_value(page, "Website:", "web.com")
    assert_field_value(page, "Branch Time Zone:", "(GMT-12:00) GMT+12, Etc")
    assert_field_value(page, "Status:", "Active")
    assert_field_value(page, "Created By:", "sohaib ahmad")

    # Address validation (combined text)
    assert_field_value(page, "Address:", "line1")
    assert_field_value(page, "Address:", "line2")
    assert_field_value(page, "Address:", "Altona")
    # assert_field_value(page, "Address:", "Manitoba")


    # assert_field_value(page, "Start Date:", TODAY_FULL)
    expected_start_date = datetime.today().strftime("%m-%d-%Y")
    assert_field_value(page, "Start Date:", expected_start_date)


    # assert_field_value(page, "End Date:", TODAY_FULL)
    expected_start_date = datetime.today().strftime("%m-%d-%Y")
    assert_field_value(page, "End Date:", expected_start_date)

def test_edit_Branch(page: Page):
    page.get_by_role("row", name=BRANCH_NAME).locator("a").first.click()
    page.wait_for_timeout(3000)

    page.locator("input[name='code']").fill(BRANCH_CODE1)

    # Branch Level
    page.locator("//input[@placeholder='Please select branch level']").click()
    page.wait_for_selector("//li[normalize-space()='Level 3']", state="visible")
    page.locator("//li[normalize-space()='Level 3']").click()

    page.locator("//input[@placeholder='Email@example.com']").fill("test@gmail.co")
    page.locator("input[name='website']").fill("web.co")

    # --- Address (opens address modal/drawer) ---
    page.locator("#vz_add_edit_modal_scroll span").nth(3).click()
    page.locator("#street").fill("updateline1")
    page.locator("#street2").fill("updateline2")

    page.locator("#postalCode").fill("66000")

    # ✅ Save ADDRESS modal specifically (first Save)
    page.wait_for_selector("text=SavePlease wait...", state="visible")
    page.get_by_text("SavePlease wait...").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox", name="Please select time zone").click()
    page.get_by_text("(GMT-11:00) GMT+11, Etc").click()

    # --- End Date (dynamic today via data-test) ---
    page.wait_for_selector("input[name='endDate']", state="visible")
    page.locator("input[name='endDate']").click()
    page.wait_for_timeout(600)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()

    # Description
    page.get_by_role("textbox", name="Description").fill("updated description test text")

    # ✅ Save MAIN Branch form (second Save) - scope to main add/edit modal
    page.get_by_role("button", name="Save").click()


# def test_activity_Branch_updated(page: Page):
#
#
#     # Open activity drawer
#     page.locator("#kt_lookup_drawer_toggle-activity").click()
#     expect(page.locator("#kt_lookup_drawer")).to_be_visible()
#
#     # Search activity
#     search_box = page.locator("#kt_lookup_drawer").get_by_role("textbox", name="Search")
#     search_box.fill(BRANCH_NAME1)
#     search_box.press("Enter")
#
#     # Get latest activity row (skip header)
#     latest_row = (page.locator("#kt_lookup_drawer").get_by_role("row").nth(1))
#
#     # Event column
#     event_cell = latest_row.locator(".text-truncate").nth(2)
#
#     # Assertions
#     expect(event_cell).to_contain_text(BRANCH_NAME1)
#     expect(event_cell).to_contain_text("updated")


# def test_verify_branch_update_activity(page: Page):
#     page.locator("#kt_lookup_drawer_toggle-activity").click()
#     drawer = page.locator("#kt_lookup_drawer")
#     expect(drawer).to_be_visible()
#
#     # Search activity
#     search_box = drawer.get_by_role("textbox", name="Search")
#     search_box.fill(BRANCH_NAME)
#     search_box.press("Enter")
#
#     # Assertions
#     expect(page.locator(f"span[title*='{BRANCH_NAME}'][title*='branch address line 2 has been updated']")).to_be_visible()
#
#     expect(page.locator(f"span[title*='{BRANCH_NAME}'][title*='branch address line 1 has been updated']")).to_be_visible()
#
#     expect(page.locator(f"span[title*='{BRANCH_NAME}'][title*='branch  postal code has been updated']")).to_be_visible()
#
#     expect(page.locator(f"span[title*='{BRANCH_NAME}'][title*='branch description has been updated']")).to_be_visible()
#
#     expect(page.locator(f"span[title*='{BRANCH_NAME}'][title*='branch email has been updated']")).to_be_visible()
#
#     expect(page.locator(f"span[title*='{BRANCH_NAME}'][title*='branch level has been updated']")).to_be_visible()
#
#     expect(page.locator(f"span[title*='{BRANCH_NAME}'][title*='branch website has been updated']")).to_be_visible()
#
#     expect(page.locator(f"span[title*='{BRANCH_NAME}'][title*='branch number has been updated']")).to_be_visible()

def test_verify_branch_update_activity(page: Page):
    page.locator("#kt_lookup_drawer_toggle-activity").click()
    drawer = page.locator("#kt_lookup_drawer")
    expect(drawer).to_be_visible()

    # Search activity
    search_box = drawer.get_by_role("textbox", name="Search")
    search_box.fill(BRANCH_NAME)
    search_box.press("Enter")

    update_messages = [
        "branch address line 2 has been updated",
        "branch address line 1 has been updated",
        "branch address postal code has been updated",
        "branch description has been updated",
        "branch email has been updated",
        "branch level has been updated",
        "branch website has been updated",
        "branch number has been updated",
    ]

    for message in update_messages:
        expect(
            page.locator(
                f'span[title*="{BRANCH_NAME}"][title*="{message}"]'
            )
        ).to_be_visible()


def test_create_and_verify_branch2(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
    # # --- Open Business → Branches ---
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Branches']", state="visible")
    # page.locator("//span[normalize-space()='Branches']").click()
    # page.wait_for_load_state("networkidle")

    # --- Add Branch ---
    page.get_by_text("Add Branch").click()

    # Fill basic fields
    page.locator("input[name='name']").fill(BRANCH_NAME2)
    page.locator("input[name='code']").fill(BRANCH_CODE2)

    # Branch Level
    page.locator("//input[@placeholder='Please select branch level']").click()
    page.get_by_role("listitem").filter(has_text="Level 1").click()

    # Email + Website
    page.locator("//input[@placeholder='Email@example.com']").fill("test@gmail.com")
    page.locator("input[name='website']").fill("web.com")

    # --- Address Modal ---
    page.locator("#vz_add_edit_modal_scroll span").nth(3).click()  # Address button

    page.locator("#street").fill("line1")
    page.locator("#street2").fill("line2")

    page.get_by_role("textbox", name="Please select country").click()
    page.get_by_role("listitem").filter(has_text="Canada").click()

    page.locator("div").filter(has_text=re.compile(r"^State/Province/Region$")).get_by_role("img").click()
    page.get_by_role("listitem").filter(has_text="Manitoba").click()

    page.locator("#kt_modal_assign_user_scroll div").filter(has_text=re.compile(r"^City$")).get_by_role("img").click()
    page.wait_for_selector("//input[@placeholder='Please select city']", state="visible").click()
    page.get_by_role("listitem").filter(has_text="Altona").click()

    page.locator("#postalCode").fill("44000")

    # Save Address
    page.get_by_text("SavePlease wait...").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox", name="Please select time zone").click()
    page.get_by_text("(GMT-12:00) GMT+12, Etc").click()

    # --- End Date ---
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()

    # Description
    page.get_by_role("textbox", name="Description").fill("description test text")

    # Save branch
    page.get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")

    # --- Verify table row ---
    assert_row_present(page, BRANCH_NAME2)


def test_create_and_verify_branch3(page: Page):
    # # --- Open Business → Branches ---
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Branches']", state="visible")
    # page.locator("//span[normalize-space()='Branches']").click()
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
    # --- Add Branch ---
    page.get_by_text("Add Branch").click()

    # Fill basic fields
    page.locator("input[name='name']").fill(BRANCH_NAME3)
    page.locator("input[name='code']").fill(BRANCH_CODE3)

    # Branch Level
    page.locator("//input[@placeholder='Please select branch level']").click()
    page.get_by_role("listitem").filter(has_text="Level 1").click()

    # Email + Website
    page.locator("//input[@placeholder='Email@example.com']").fill("test@gmail.com")
    page.locator("input[name='website']").fill("web.com")

    # --- Address Modal ---
    page.locator("#vz_add_edit_modal_scroll span").nth(3).click()  # Address button

    page.locator("#street").fill("line1")
    page.locator("#street2").fill("line2")

    page.get_by_role("textbox", name="Please select country").click()
    page.get_by_role("listitem").filter(has_text="Canada").click()

    page.locator("div").filter(has_text=re.compile(r"^State/Province/Region$")).get_by_role("img").click()
    page.get_by_role("listitem").filter(has_text="Manitoba").click()

    page.locator("#kt_modal_assign_user_scroll div").filter(has_text=re.compile(r"^City$")).get_by_role("img").click()
    page.wait_for_selector("//input[@placeholder='Please select city']", state="visible").click()
    page.get_by_role("listitem").filter(has_text="Altona").click()

    page.locator("#postalCode").fill("44000")

    # Save Address
    page.get_by_text("SavePlease wait...").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox", name="Please select time zone").click()
    page.get_by_text("(GMT-12:00) GMT+12, Etc").click()

    # --- End Date ---
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()

    # Description
    page.get_by_role("textbox", name="Description").fill("description test text")

    # Save branch
    page.get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")

    # --- Verify table row ---
    assert_row_present(page, BRANCH_NAME3)


# def test_multi_delete_Branch(page: Page):
#     page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
#     page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
#     page.wait_for_load_state("networkidle")
#     page.get_by_role("row", name=BRANCH_NAME2).get_by_role("checkbox").check()
#     page.get_by_role("row", name=BRANCH_NAME3).get_by_role("checkbox").check()
#     page.get_by_role("button", name="Delete Selected").click(button="left")
#     page.locator("//button[normalize-space()='Delete']").click()
#     expect(BRANCH_NAME2).not_to_be_visible()
#     expect(BRANCH_NAME3).not_to_be_visible()
def test_multi_delete_Branch(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
    table = page.locator("table").first
    # branch2 = page.get_by_role("row", name=BRANCH_NAME2)
    # branch3 = page.get_by_role("row", name=BRANCH_NAME3)
    page.get_by_role("row", name=BRANCH_NAME2).get_by_role("checkbox").check()
    page.get_by_role("row", name=BRANCH_NAME3).get_by_role("checkbox").check()

    page.get_by_role("button", name="Delete Selected").click()
    page.locator("//button[normalize-space()='Delete']").click()

    # Assert deleted branches are NOT visible in the list


    # expect(branch2).not_to_be_visible()
    # expect(branch3).not_to_be_visible()
    expect(table.get_by_role("row", name=BRANCH_NAME2)).to_have_count(0)
    expect(table.get_by_role("row", name=BRANCH_NAME3)).to_have_count(0)


def test_create_and_verify_branch4(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
    # # --- Open Business → Branches ---
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Branches']", state="visible")
    # page.locator("//span[normalize-space()='Branches']").click()
    # page.wait_for_load_state("networkidle")

    # --- Add Branch ---
    page.get_by_text("Add Branch").click()

    # Fill basic fields
    page.locator("input[name='name']").fill(BRANCH_NAME4)
    page.locator("input[name='code']").fill(BRANCH_CODE4)

    # Branch Level
    page.locator("//input[@placeholder='Please select branch level']").click()
    page.get_by_role("listitem").filter(has_text="Level 1").click()

    # Email + Website
    page.locator("//input[@placeholder='Email@example.com']").fill("test@gmail.com")
    page.locator("input[name='website']").fill("web.com")

    # --- Address Modal ---
    page.locator("#vz_add_edit_modal_scroll span").nth(3).click()  # Address button

    page.locator("#street").fill("line1")
    page.locator("#street2").fill("line2")

    page.get_by_role("textbox", name="Please select country").click()
    page.get_by_role("listitem").filter(has_text="Canada").click()

    page.locator("div").filter(has_text=re.compile(r"^State/Province/Region$")).get_by_role("img").click()
    page.get_by_role("listitem").filter(has_text="Manitoba").click()

    page.locator("#kt_modal_assign_user_scroll div").filter(has_text=re.compile(r"^City$")).get_by_role("img").click()
    page.wait_for_selector("//input[@placeholder='Please select city']", state="visible").click()
    page.get_by_role("listitem").filter(has_text="Altona").click()

    page.locator("#postalCode").fill("44000")

    # Save Address
    page.get_by_text("SavePlease wait...").click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox", name="Please select time zone").click()
    page.get_by_text("(GMT-12:00) GMT+12, Etc").click()

    # --- End Date ---
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()

    # Description
    page.get_by_role("textbox", name="Description").fill("description test text")

    # Save branch
    page.get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")

    # --- Verify table row ---
    assert_row_present(page, BRANCH_NAME4)


# def test_single_delete_Branch(page: Page):
#     page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
#     page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
#     page.get_by_role("row", name=BRANCH_NAME4).locator("a").nth(1).click()
#     page.get_by_role("button", name="Delete").click()
#     expect(BRANCH_NAME4).not_to_be_visible()
def test_single_delete_Branch(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
    table = page.locator("table").first
    # deleted_branch = page.get_by_role("row", name=BRANCH_NAME4)
    # Open row action menu
    page.get_by_role("row", name=BRANCH_NAME4).locator("a").nth(1).click()

    # Click Delete
    page.get_by_role("button", name="Delete").click()

    # Assert deleted branch is no longer visible
    expect(table.get_by_role("row", name=BRANCH_NAME4)).to_have_count(0)
    # expect(deleted_branch).not_to_be_visible()


# def test_activity_Branch_deleted(page: Page):
#     # Open activity drawer
#     page.locator("#kt_lookup_drawer_toggle-activity").click()
#     expect(page.locator("#kt_lookup_drawer")).to_be_visible()
#
#     # Search activity
#     search_box = page.locator("#kt_lookup_drawer").get_by_role(
#         "textbox", name="Search"
#     )
#     search_box.fill("test_branch_vumjqi")
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
#     expect(event_cell).to_contain_text("test_branch_vumjqi")
#     expect(event_cell).to_contain_text("deleted")


def test_search_Branch(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
    page.get_by_role("textbox", name='Search').first.click()
    page.get_by_role("textbox", name="Search").first.type('test_branch_owhbpd')
    page.get_by_role("textbox", name="Search").first.press("Enter")

    # Positive assertion
    branch_search = page.locator(
        "span.text-truncate",
        has_text="test_branch_owhbpd"
    )
    expect(branch_search).to_be_visible()

    # Negative assertion
    other_branch = page.locator(
        "span.text-truncate",
        has_text="Mcdonalds (johar town)"
    )
    expect(other_branch).not_to_be_visible()


# def test_filter_Branch(page: Page):
#
#     page.wait_for_timeout(5000)
#     page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
#
#     page.get_by_role("button", name=" Filter 1").click()
#
#     filter_panel = page.locator("div").filter(has_text="Filter Options")
#
#     # Now find State field ONLY inside filter panel
#     state_field = filter_panel.get_by_text("State:").locator("..").locator("div.multiselect-tags")
#     state_field.click()
#
#     state_field.locator("input").fill("Manitoba")
#     page.locator("span", has_text="Manitoba").click()
#
#     page.get_by_role("button", name="Apply").click()
#
#     # ✅ Assertion: only Manitoba branches should be visible
#     results = page.locator("span.text-truncate")
#     expect(results).to_contain_text("Manitoba")
#
#     page.get_by_role("button", name="Apply").click()
#
#
#
#     page.get_by_role("button", name=" Filter 4").click()
#     page.get_by_role("button", name="Reset").click()


def test_clone_Branch(page: Page):
    page.wait_for_timeout(6000)
    # page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.goto("https://vyzor.app/#/branch", wait_until="networkidle")
    page.get_by_role("row", name="test_branch_owhbpd").get_by_role("button").click()
    page.get_by_role("menuitem", name="Clone").click()
    # page.get_by_role("button", name="Clone").click()
    page.locator("input[name=\"name\"]").click()
    page.locator("input[name=\"name\"]").fill(clone)
    page.locator("input[name=\"code\"]").click()
    page.locator("input[name=\"code\"]").fill(BRANCH_CODE5)
    page.get_by_role("textbox", name="Please select branch").click()
    page.get_by_role("listitem").filter(has_text="Level 3").click()
    page.get_by_role("textbox", name="Email@example.com").click()
    page.get_by_role("textbox", name="Email@example.com").fill("test@test.com")
    page.locator("input[name=\"website\"]").click()
    page.locator("input[name=\"website\"]").fill("dsf")
    page.get_by_role("cell", name="Address* ").locator("span").click()
    page.locator("#street").click()
    page.locator("#street").fill("line 1")
    page.locator("#street2").click()
    page.locator("#street2").fill("line2")
    page.get_by_role("textbox", name="Please select country").click()
    page.get_by_role("textbox", name="Canada").fill("ca")
    page.get_by_role("listitem").filter(has_text="Canada").click()
    page.get_by_role("textbox", name="Please select state/province/").click()
    page.get_by_role("listitem").filter(has_text="Alberta").click()
    page.get_by_role("textbox", name="Please select city").click()
    page.get_by_role("listitem").filter(has_text="Airdrie").click()
    page.locator("#postalCode").click()
    page.locator("#postalCode").fill("3455")
    page.get_by_text("SavePlease wait...").click()
    page.get_by_role("textbox", name="Please select time zone").click()
    page.get_by_text("(GMT-12:00) GMT+12, Etc").click()
    # page.get_by_role("cell", name="End Date", exact=True).get_by_placeholder("Select date").click()
    # # page.locator("[data-test=\"Thu Apr 30 2026 00:00:00 GMT+0500 (Pakistan Standard Time)\"]").get_by_text(
    # #     "30").click()
    # page.get_by_role("row", name="Saturday -", exact=True).get_by_label("").check()
    # page.get_by_role("row", name="Sunday -", exact=True).get_by_label("").check()
    # page.locator("textarea[name=\"description\"]").click()
    page.get_by_role("row", name="Saturday -", exact=True).get_by_label("").check()
    page.get_by_role("row", name="Sunday -", exact=True).get_by_label("").check()
    page.locator("textarea[name=\"description\"]").fill("were")
    page.get_by_role("button", name="Save").click()
    assert_row_present(page, clone)
