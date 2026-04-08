# tests/test_create_branch.py
import re
import pytest
from playwright.sync_api import Page
from test_data import BRANCH_NAME, BRANCH_CODE, TODAY_FULL, SECTION_NAME, LOCATION_NAME, TODAY_DAY, START_DATE_FULL, \
    START_DATE_DAY, END_DATE_FULL, END_DATE_DAY, FORM_NAME, FORM_START_FULL, FORM_START_DAY, FORM_END_FULL, \
    FORM_END_DAY, USER_FIRST_NAME, EMAIL, START_DATETIME, CHAT_NAME, EVENT_NAME, LOOKUP_NAME, BRANCH_NAME1, \
    BRANCH_CODE1, LOCATION_NAME1, FORM_NAME1, ROLE_NAME, END_DATETIME
from conftest import assert_row_present


# @pytest.mark.order(1)
# def test_valid_login(page: Page):
#     page.goto("https://vyzor.app/#/sign-in", wait_until="networkidle")
#
#     # --- Valid Login ---
#     page.wait_for_selector("input[name='username']", state="visible")
#     page.locator("input[name='username']").fill("sohaib2@vyzor.com")
#
#     page.wait_for_selector("input[type='password']", state="visible")
#     page.locator("input[type='password']").fill("Password@355")
#
#     # page.wait_for_selector("button:has-text('Log in')")
#     page.get_by_role("button", name="Log in").click()


@pytest.mark.order(2)
def test_create_branch(page: Page):
    # --- Open Business → Branches ---
    page.wait_for_selector("#BusinessBusiness", state="visible")
    page.locator("#BusinessBusiness").click()
    page.wait_for_selector("//span[normalize-space()='Branches']", state="visible")
    page.locator("//span[normalize-space()='Branches']").click()
    page.wait_for_load_state("networkidle")

    # --- Add Branch ---
    page.get_by_text("Add Branch").click()
    page.wait_for_timeout(2000)  # modal animation

    # Fill form (shared variables)
    page.locator("input[name='name']").fill(BRANCH_NAME)
    page.locator("input[name='code']").fill(BRANCH_CODE)

    # Branch Level
    page.locator("//input[@placeholder='Please select branch level']").click()
    page.wait_for_selector("//li[normalize-space()='Level 1']", state="visible")
    page.locator("//li[normalize-space()='Level 1']").click()

    page.locator("//input[@placeholder='Email@example.com']").fill("test@gmail.com")
    page.locator("input[name='website']").fill("web.com")

    # --- Address (opens address modal/drawer) ---
    page.locator("#vz_add_edit_modal_scroll span").nth(3).click()
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

    # ✅ Save ADDRESS modal specifically (first Save)
    page.wait_for_selector("text=SavePlease wait...", state="visible")
    page.get_by_text("SavePlease wait...").click()
    page.wait_for_timeout(5000)
    page.get_by_role("textbox", name="Please select time zone").click()
    page.get_by_text("(GMT-12:00) GMT+12, Etc").click()

    # --- End Date (dynamic today via data-test) ---
    page.wait_for_selector("input[name='endDate']", state="visible")
    page.locator("input[name='endDate']").click()
    page.wait_for_timeout(600)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()

    # Description
    page.get_by_role("textbox", name="Description").fill("description test text")

    # ✅ Save MAIN Branch form (second Save) - scope to main add/edit modal
    page.get_by_role("button", name="Save").click()
    page.wait_for_load_state("networkidle")
    page.get_by_title(BRANCH_NAME, exact=True).locator("span").click()
    page.locator("[id=\"tab-site.user\"]").get_by_text("Users").click()
    page.get_by_role("button", name="Assign Role").click()
    page.get_by_role("textbox", name="Please select role").click()
    page.get_by_role("listitem").filter(has_text="Site Admin").click()
    page.get_by_role("button", name="Save").click()
    page.locator("#vz__drawer_close").click()

    # --- Verify in table (row check) ---
    assert_row_present(page, BRANCH_NAME)

    page.get_by_role("row", name=BRANCH_NAME).locator("a").first.click()
    page.wait_for_timeout(3000)
    page.locator("input[name='name']").fill(BRANCH_NAME1)
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
    assert_row_present(page, BRANCH_NAME1)


@pytest.mark.order(3)
def test_create_location(page: Page):
    page.goto("https://vyzor.app/#/locations", wait_until="networkidle")
    page.wait_for_timeout(3000)
    # # --- Navigate to Locations ---
    # page.wait_for_selector("#BusinessBusiness", state="visible")
    # page.locator("#BusinessBusiness").click()
    # page.wait_for_selector("//span[normalize-space()='Locations']", state="visible")
    # page.wait_for_timeout(1500)
    #
    # page.locator("//span[normalize-space()='Locations']").click()
    # page.wait_for_load_state("networkidle")
    # page.wait_for_timeout(2000)

    # --- Add Location ---
    page.get_by_text("Add Location").click()
    page.wait_for_timeout(2000)

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
    page.get_by_role("option", name=BRANCH_NAME1).locator("span").first.click()

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

    page.get_by_role("row", name=LOCATION_NAME).locator("a").first.click()
    page.locator("input[name='name']").fill(LOCATION_NAME1)
    page.locator("div[role='dialog']").get_by_role("button", name="Save").click()
    page.wait_for_timeout(1500)
    assert_row_present(page, LOCATION_NAME1)


@pytest.mark.order(4)
def test_create_form(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.wait_for_timeout(2000)

    page.get_by_text("Templates").click()
    page.get_by_role("link", name=" Forms").click()
    page.get_by_role("link", name=" Add Form").click()
    page.locator("input[name=\"formName\"]").click()
    page.locator("input[name=\"formName\"]").fill(FORM_NAME)
    page.get_by_text("Please select category").dblclick()
    page.get_by_role("option", name="Service").locator("span").first.click()
    # Start = today
    page.locator("input[name='startDate']").click()
    page.locator(f"[data-test*='{FORM_START_FULL}']").get_by_text(FORM_START_DAY).click()

    # End = today + 1
    page.locator("input[name='endDate']").click()
    page.locator(f"[data-test*='{FORM_END_FULL}']").get_by_text(FORM_END_DAY).click()

    # Continue to next step
    page.get_by_role("button", name="Continue").click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("row", name=BRANCH_NAME1).get_by_role("checkbox").check()
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name=" Users").click()
    page.get_by_role("row", name="sohaib ahmad sohaib2@vyzor.").get_by_role("checkbox").check()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name=" Branches").click()
    page.get_by_role("button", name="Save").click()

    assert_row_present(page, FORM_NAME)

    page.get_by_role("row", name=FORM_NAME).locator("a").first.click()
    page.wait_for_timeout(2000)
    page.locator("input[name=\"formName\"]").click()
    page.locator("input[name=\"formName\"]").fill(FORM_NAME1)
    page.locator("div").filter(has_text=re.compile(r"^Service$")).first.click()
    page.get_by_role("option", name="Select All").locator("span").first.click()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Save").click()
    assert_row_present(page, FORM_NAME1)


@pytest.mark.order(5)
def test_create_user(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.locator("#UsersUsers").click()
    page.get_by_role("link", name=" Users").click()
    page.get_by_role("link", name=" Add User").click()
    page.wait_for_timeout(1000)
    page.locator("input[name=\"firstName\"]").click()
    page.locator("input[name=\"firstName\"]").fill(USER_FIRST_NAME)
    page.wait_for_timeout(1000)
    page.locator("input[name=\"lastName\"]").click()
    page.locator("input[name=\"lastName\"]").fill("auto")
    page.get_by_role("textbox", name="Email@example.com").click()
    page.get_by_role("textbox", name="Email@example.com").fill(EMAIL)
    page.wait_for_timeout(1000)
    page.get_by_role("textbox", name="Date of birth").click()
    page.get_by_role("button", name="Open years overlay").click()
    page.get_by_text("1996").click()
    page.locator("[data-test=\"Mon Nov 04 1996 00:00:00 GMT+0500 (Pakistan Standard Time)\"]").get_by_text("4").click()
    page.locator("//input[@name='password']").click()
    page.locator("//input[@name='password']").fill("Password@355")
    page.locator("//input[@name='password_confirmation']").click()
    page.locator("//input[@name='password_confirmation']").fill("Password@355")
    page.get_by_role("textbox", name="Start Date").click()
    page.wait_for_timeout(600)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.get_by_role("textbox", name="End Date").click()
    page.wait_for_timeout(600)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.get_by_role("textbox", name="Enter a phone number").click()
    page.get_by_role("textbox", name="Enter a phone number").fill("03334170000")
    page.get_by_text("Assign Branch").click()
    page.locator("div").filter(has_text=re.compile(r"^Please select branch$")).click()
    page.get_by_role("option", name=BRANCH_NAME1).locator("span").first.click()
    page.locator("#kt_modal_create_user_add_site").get_by_role("img").click()
    page.get_by_role("listitem").filter(has_text="Site Admin").click()
    page.wait_for_timeout(1000)
    page.locator("#kt_modal_create_user_add_site").get_by_role("button", name="Save").click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Save").click()
    page.wait_for_timeout(1000)

    assert_row_present(page, USER_FIRST_NAME)


@pytest.mark.order(6)
def test_create_form_schedule(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.get_by_text("Applications").click()
    page.get_by_role("link", name=" Scheduler").click()
    page.get_by_role("button", name=" Add Task").click()
    page.get_by_role("textbox", name="Branch").click()
    page.wait_for_timeout(2000)
    page.get_by_role("listitem").filter(has_text=BRANCH_NAME1).click()
    page.wait_for_timeout(2000)
    page.get_by_role("textbox", name="Users/Roles").click()
    page.wait_for_timeout(2000)
    page.get_by_role("listitem").filter(has_text="sohaib ahmad").click()
    page.get_by_role("textbox", name="Form").click()

    page.get_by_role("listitem").filter(has_text=FORM_NAME1).click()

    # inside your test file

    page.get_by_role("textbox", name="Select start date").click()
    page.get_by_role("textbox", name="Select start date").fill(START_DATETIME)
    page.get_by_role("button", name="OK").click()
    page.get_by_role("textbox", name="Select end date").click()
    page.get_by_role("textbox", name="Select end date").fill(END_DATETIME)

    page.get_by_role("button", name="Save").click()


@pytest.mark.order(7)
def test_create_chat(page: Page):
    page.goto("https://vyzor.app/#/chat")
    page.wait_for_timeout(2000)

    # page.wait_for_selector("button:has-text('Log in')", state="visible")
    # page.get_by_role("button", name="Log in").click()
    # page.wait_for_load_state("networkidle")
    # page.locator("#TemplatesTemplates").click()
    # page.get_by_text("Applications").click()
    # page.get_by_role("link", name=" Chat").click()
    page.get_by_text("Add", exact=True).click()
    page.locator("#title").click()
    page.locator("#title").fill(CHAT_NAME)
    page.locator("div").filter(has_text=re.compile(r"^Please select user$")).click()
    page.get_by_role("option", name="sohaib ahmad").locator("span").first.click()
    page.get_by_role("button", name="Save").click()
    page.wait_for_timeout(2000)

    chat_after_save = page.locator(f"//a[normalize-space()='{CHAT_NAME}']").all_inner_texts()

    # Verify if CHAT_NAME appears in the text list
    if CHAT_NAME in chat_after_save:
        print(f"✅ Test Passed: Chat '{CHAT_NAME}' found in chat list!")
    else:
        print(f"❌ Test Failed: Chat '{CHAT_NAME}' not found!")


@pytest.mark.order(8)
def test_create_event(page: Page):
    page.goto("https://vyzor.app/#/branch-dashboard", wait_until="networkidle")
    page.wait_for_timeout(2000)

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
    page.locator(
        "//li[contains(@class,'el-select-dropdown__item')]//span[normalize-space()='Scheduled Event']").click()

    page.get_by_role("textbox", name="Provider").click()
    page.get_by_role("listitem").filter(has_text="Vyzor Email Provider").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Save").click()
    # ---------------------
    assert_row_present(page, EVENT_NAME)


@pytest.mark.order(9)
def test_create_lookup(page: Page):
    page.goto("https://vyzor.app/#/lookup")
    page.wait_for_timeout(2000)
    # page.locator("#SettingsSettings").get_by_text("Settings").click()
    # page.get_by_role("link", name=" Lookup Configuration").click()
    page.get_by_text("Add Lookup").click()
    page.locator("input[name=\"lookupName\"]").click()
    page.locator("input[name=\"lookupName\"]").fill(LOOKUP_NAME)
    page.locator("input[name=\"startDate\"]").click()
    page.wait_for_timeout(1000)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.wait_for_timeout(1000)
    page.locator("input[name=\"endDate\"]").click()
    page.wait_for_timeout(1000)
    page.locator(f"[data-test*='{TODAY_FULL}']").get_by_text(str(TODAY_DAY)).click()
    page.get_by_role("button", name="Save").click()
    assert_row_present(page, LOOKUP_NAME)


@pytest.mark.order(10)
def test_create_role(page: Page):
    page.wait_for_timeout(2000)
    page.goto("https://vyzor.app/#/roles")

    # page.locator("#UsersUsers").click()
    # page.get_by_role("link", name=" Roles").click()
    page.get_by_text("Add Role").click()
    page.locator("#roleName").click()
    page.locator("#roleName").fill(ROLE_NAME)
    page.get_by_role("button", name="Save").click()
    page.wait_for_timeout(2000)

    role_after_save = page.locator(f"//a[normalize-space()='{ROLE_NAME}']").all_inner_texts()

    if ROLE_NAME in role_after_save:
        print(f"✅ Test Passed: Role '{ROLE_NAME}' found in Role list!")
    else:
        print(f"❌ Test Failed: Role '{ROLE_NAME}' not found!")
    page.wait_for_timeout(2000)


@pytest.mark.order(11)
def test_create_section_edit(page: Page):
    page.goto("https://vyzor.app/#/sections")
    page.wait_for_timeout(2000)

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
    page.get_by_role("row",
                     name=re.compile(f"{SECTION_NAME}.*{TODAY_DAY}")).get_by_role(
        "link").click()

    page.locator("div").filter(has_text=re.compile(r"^Rows$")).get_by_role(
        "spinbutton").click()
    page.locator("div").filter(has_text=re.compile(r"^Rows$")).get_by_role(
        "spinbutton").fill("4")
    page.locator("div").filter(
        has_text=re.compile(r"^Columns\(Max 6\)$")).get_by_role(
        "spinbutton").click()
    page.locator("div").filter(
        has_text=re.compile(r"^Columns\(Max 6\)$")).get_by_role("spinbutton").fill(
        "3")
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
