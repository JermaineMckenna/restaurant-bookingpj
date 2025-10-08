# project3rb/homepageapp/google_calendar.py

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

if GOOGLE_CREDS:
    info = json.loads(GOOGLE_CREDS)
    credentials = service_account.Credentials.from_service_account_info(
        info,
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    service = build('calendar', 'v3', credentials=credentials)
else:
    credentials = None
    service = None


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
