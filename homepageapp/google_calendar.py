import os
import json
from datetime import datetime, timedelta
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Calendar setup
CALENDAR_ID = 'restaurantbookingproject@restaurant-booking-calendar.iam.gserviceaccount.com'
TIMEZONE = 'Europe/London'

# Load credentials from environment variable (Heroku)
GOOGLE_CREDS = os.environ.get("GOOGLE_CREDS")

credentials = None
service = None

if GOOGLE_CREDS:
    try:
        # Ensure JSON string is converted to dict
        info = json.loads(GOOGLE_CREDS)
        credentials = service_account.Credentials.from_service_account_info(
            info,
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        service = build('calendar', 'v3', credentials=credentials)
        print("✅ Google Calendar connected successfully.")
    except Exception as e:
        print(f"⚠️ Failed to load Google credentials: {e}")
else:
    print("⚠️ GOOGLE_CREDS environment variable not found.")


def create_event(title, start_datetime, end_datetime, description=''):
    """
    Creates a new event in the Google Calendar.
    """
    if not service:
        print("⚠️ Google Calendar service not configured.")
        return None

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': TIMEZONE,
        },
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event