# playwright.config.py

def pytest_playwright_config(playwright, config):
    return {
        "use": {
            "headless": False,
            "viewport": {"width": 1366, "height": 768},
            "actionTimeout": 50000,
            "navigationTimeout": 60000,
            "ignoreHTTPSErrors": True,
            "screenshot": "only-on-failure",
            "video": "retain-on-failure",
        }
    }
