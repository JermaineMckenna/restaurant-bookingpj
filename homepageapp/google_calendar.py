import os
import json
from datetime import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ------------------------------------------------
# Google Calendar Settings
# ------------------------------------------------
CALENDAR_ID = 'restaurantbookingproject@restaurant-booking-calendar.iam.gserviceaccount.com'
TIMEZONE = 'Europe/London'

# Try to load credentials from Heroku config var
GOOGLE_CREDS = os.environ.get("GOOGLE_CREDS")

credentials = None
service = None

if GOOGLE_CREDS:
    try:
        # If the value is a string, convert to dictionary
        creds_dict = json.loads(GOOGLE_CREDS) if isinstance(GOOGLE_CREDS, str) else GOOGLE_CREDS

        # Create credentials from the dictionary
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/calendar']
        )

        # Build Google Calendar service
        service = build('calendar', 'v3', credentials=credentials)
        print("✅ Google Calendar connection successful.")
    except json.JSONDecodeError:
        print("⚠️ GOOGLE_CREDS could not be decoded. Make sure it’s valid JSON.")
    except Exception as e:
        print(f"⚠️ Error setting up Google Calendar: {e}")
else:
    print("⚠️ GOOGLE_CREDS environment variable not found.")


def create_event(title, start_datetime, end_datetime, description=''):
    """
    Create a new event in Google Calendar.
    """
    if not service:
        print("⚠️ Google Calendar service not available.")
        return None

    try:
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
        print(f"✅ Event created: {created_event.get('htmlLink')}")
        return created_event

    except Exception as e:
        print(f"⚠️ Failed to create Google Calendar event: {e}")
        return None