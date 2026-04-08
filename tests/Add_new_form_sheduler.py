import re
import pytest
from playwright.sync_api import Page
from test_data import (
    START_DATETIME,
    END_DATE


)
BRANCH_NAME = "test_branch_owhbpd"
FORM_NAME='Automation_pkchoz'
def test_create_form_shedule(page: Page):


    page.wait_for_load_state("networkidle")
    # page.get_by_text("Applications").click()
    # page.get_by_role("link", name=" Scheduler").click()
    page.wait_for_timeout(4000)
    page.goto("https://vyzor.app/#/scheduler")
    page.get_by_role("button", name=" Add Task").click()
    page.get_by_role("textbox", name="Branch").click()

    page.get_by_role("listitem").filter(has_text=BRANCH_NAME).click()
    page.get_by_role("textbox", name="Users/Roles").click()
    page.get_by_role("listitem").filter(has_text="sohaib ahmad").click()
    page.get_by_role("textbox", name="Form").click()
    page.get_by_role("listitem").filter(has_text=FORM_NAME).click()

    # inside your test file

    page.get_by_role("textbox", name="Select start date").click()
    page.get_by_role("textbox", name="Select start date").fill(START_DATETIME)
    page.get_by_role("button", name="OK").click()
    page.get_by_role("textbox", name="Select end date").click()
    page.get_by_role("textbox", name="Select end date").fill(START_DATETIME)

    page.get_by_role("button", name="Save").click()


