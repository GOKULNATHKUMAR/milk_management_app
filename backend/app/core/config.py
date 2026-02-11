import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/app/.env")
CRON_SECRET = "milk_app_daily_summary_9pm_secret_2026"
#CRON_SECRET = os.getenv("CRON_SECRET")

print(f"CRON_SECRET loaded: {CRON_SECRET is not None}")
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/milk_app"
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql://postgres:postgres@localhost:5432/milk_app"
# )