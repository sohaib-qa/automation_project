import re
import pytest
from playwright.sync_api import Page, expect
from test_data import (
    CHAT_NAME

)



def test_create_chat(page: Page):
    page.goto("https://vyzor.app/#/chat/")
    page.wait_for_load_state("networkidle")

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

    chat_after_save = page.locator("//a[normalize-space()='chat jeru']").all_inner_texts()

    # Verify if CHAT_NAME appears in the text list
    if CHAT_NAME in chat_after_save:
        print(f"✅ Test Passed: Chat '{CHAT_NAME}' found in chat list!")
    else:
        print(f"❌ Test Failed: Chat '{CHAT_NAME}' not found!")


def test_chat_filter(page: Page):
    page.reload()
    page.locator("//i[@class='las la-filter fs-1']").click()
    # page.locator("#vz-filter-data-smsFilters div").filter(has_text=re.compile(r"^Select option$")).click()
    # page.get_by_role("option", name="Sohaib Ahmad", exact=True).locator("span").first.click()
    # page.get_by_role("button", name="Apply").click()
    # page.locator("//i[@class='las la-filter fs-1']").click()
    # page.get_by_role("button", name="Reset").click()
    page.get_by_role("combobox").filter(has_text="Select optionSelect").locator("div").first.click()
    page.get_by_role("textbox", name="Select option").click()
    page.get_by_role("textbox", name="Select option").type("sohaib")
    page.get_by_role("option", name="sohaib ahmad", exact=True).locator("span").first.click()
    page.get_by_role("button", name="Apply").click()
    page.locator("//i[@class='las la-filter fs-1']").click()
    page.get_by_role("button", name="Reset").click()




def test_chat_search(page: Page):
    page.reload()
    search_box = page.get_by_role("textbox", name="Search", exact=True)
    search_box.fill(CHAT_NAME)
    search_box.press("Enter")

    # Wait for list update
    expect(page.locator("div.hoverClass").first).to_be_visible()

    chat_search = page.locator("div.hoverClass", has_text=CHAT_NAME)
    expect(chat_search).to_be_visible()



def test_chat_delete(page: Page):
    page.locator("div.hoverClass",has_text=CHAT_NAME).locator("input[type='checkbox']").check()
    # page.locator("div.hoverClass", has_text="Automation_nebg").locator("input[type='checkbox']").check()
    page.get_by_role("button", name=" Delete").click()
    page.get_by_role("button", name="Delete", exact=True).click()
