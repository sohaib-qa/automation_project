# # tests/test_create_branch.py
# import re
# import pytest
# from playwright.sync_api import Page
#
#
# @pytest.mark.order(1)
# def test_create_branch(logged_in_page: Page):
#     page = logged_in_page
#     page.locator("#UsersUsers").click()
#     page.locator(".form-input-unchecked").first.check()
#     page.get_by_role("button", name="Business").click()
#     page.locator("#formSwitch_852703").check()
#     page.locator("#formSwitch_3034902").check()
#     page.locator("#formSwitch_3034902").click()
#     page.locator("#formSwitch_852705").check()
#     page.locator("#formSwitch_3034902").check()
#     page.locator("#formSwitch_3034903").check()
#     page.get_by_role("row", name="Locations", exact=True).locator("div").nth(2).check()
#     page.locator("#formSwitch_3034905").check()
#     page.locator("#formSwitch_3034904").check()
#     page.locator("#formSwitch_65454").check()
#     page.locator("#formSwitch_65455").check()
#     page.locator("#formSwitch_65456").check()
#     page.locator("#formSwitch_65457").check()
#     page.locator("#kt_customer_view_payment_method div").filter(has_text="DashboardPermissionsReadCreateUpdateDeleteUser StatisticsPerformance").get_by_role("checkbox").check()
#     page.locator("div").filter(has_text=re.compile(r"^IntegrationsPermissionsReadCreateUpdateDeleteEmail ConfigurationDevices$")).get_by_role("checkbox").check()
#     page.locator("div").filter(has_text=re.compile(r"^Loading\.\.\.$")).check()
#     page.locator("div").filter(has_text=re.compile(r"^Loading\.\.\.$")).check()
#     page.locator("div").filter(has_text=re.compile(r"^SettingsPermissionsReadCreateUpdateDeleteLookup ConfigurationEvents$")).get_by_role("checkbox").check()
#     page.locator("div").filter(has_text=re.compile(r"^Loading\.\.\.$")).check()
#     page.locator("div").filter(has_text=re.compile(r"^Loading\.\.\.$")).check()
#     page.locator("div").filter(has_text=re.compile(r"^Loading\.\.\.$")).check()
#     page.locator("div").filter(has_text=re.compile(r"^TemplatesPermissionsReadCreateUpdateDeleteFormsSectionsTasks$")).get_by_role("checkbox").check()
#     page.locator("div").filter(has_text=re.compile(r"^UsersPermissionsReadCreateUpdateDeleteUsersRolesPermissionsUser Permissions$")).get_by_role("checkbox").check()
