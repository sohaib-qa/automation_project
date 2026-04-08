# tests/test_data.py
from datetime import datetime, timedelta
import random
import string

# --- login creds ---
ADMIN_EMAIL = "sohaib2@vyzor.com"
ADMIN_PASSWORD = "Password@355"


# --- small random id for unique names (Option B you chose) ---
def rid(n: int = 6) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


# --- names used across tests (feel free to add more) ---
BRANCH_NAME = f"test_branch_{rid()}"
BRANCH_NAME1 = f"Automation_branch_{rid()}"
USER_FIRST_NAME = f"{rid()}"
EMAIL = f"{rid()}@vyzor.com"
ROLE_NAME = f"Automation_{rid(4)}"

FORM_NAME1 = f"Automation_{rid()}"
EVENT_NAME = f"{rid()}"
LOOKUP_NAME = f"LK{rid()}"
SECTION_NAME = f"Automation_{rid()}"
# LOOKUP_NAME = f"lookup_{rid()}"
# Random alphabet-only location name
LOCATION_NAME = f"Automation_{rid(4)}"
LOCATION_NAME1 = f"Automation_{rid(4)}"
CHAT_NAME = f"Automation_{rid(4)}"

BRANCH_CODE = str(random.randint(10000, 99999))
BRANCH_CODE1 = str(random.randint(10000, 99999))

# --- Forms ---
FORM_NAME = f"Automation_{rid(5)}"  # random alphabet-only (e.g., form_abxyz)
FORM_CATEGORY = "General"  # update if you use a different category

# Dates: start today, end +1 day (used by form wizard)

FORM_START_FULL = datetime.now().strftime("%a %b %d %Y")
FORM_START_DAY = str(datetime.now().day)
FORM_END_FULL = (datetime.now() + timedelta(days=1)).strftime("%a %b %d %Y")
FORM_END_DAY = str((datetime.now() + timedelta(days=1)).day)

# Branch to assign the form to (you said: use BRANCH_NAME)
# BRANCH_NAME already exists in your file

# ---- Roles (choose one style) ----
# If IDs are stable, put them here (strings with the id attribute)
ROLE_IDS = [
    # "roles_checkbox_7225302",
    # "roles_checkbox_7316413",
]

# Or select by visible text on the checkbox label (recommended)
ROLE_LABELS = [
    # "Operator",
    # "Supervisor",
]

# --- dates you might need (different formats) ---
TODAY_FULL = datetime.now().strftime("%a %b %d %Y")  # e.g., "Mon Nov 03 2025"
TODAY_DMY = datetime.now().strftime("%d/%m/%Y")  # e.g., "03/11/2025"
TODAY_YMD = datetime.now().strftime("%Y-%m-%d")  # e.g., "2025-11-03"
TODAY_DAY = datetime.now().day  # numeric day

START_DATE_FULL = datetime.now().strftime("%a %b %d %Y")
START_DATE_DAY = str(datetime.now().day)

END_DATE_FULL = (datetime.now() + timedelta(days=1)).strftime("%a %b %d %Y")
END_DATE_DAY = str((datetime.now() + timedelta(days=1)).day)

# test_data.py


START_DATE = (datetime.now()).strftime("%m-%d-%Y %I:%M %p")
END_DATE = (datetime.now() + timedelta(days=2)).strftime("%m-%d-%Y %I:%M %p")

# Current time + 5 minutes
START_DATETIME = (datetime.now() + timedelta(minutes=5)).strftime("%m-%d-%Y %I:%M %p")

# End date same as start date (can change if needed later)
END_DATETIME = (datetime.now() + timedelta(minutes=55)).strftime("%m-%d-%Y %I:%M %p")
