# project3rb/homepageapp/google_calendar.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz


SERVICE_ACCOUNT_FILE = 'project3rb/credentials.json'

#
CALENDAR_ID = 'restaurantbookingproject@restaurant-booking-calendar.iam.gserviceaccount.com'

# Optional default timezone
TIMEZONE = 'Europe/London'

# Authenticate with the Google Calendar API using the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/calendar']
)

service = build('calendar', 'v3', credentials=credentials)


def create_event(title, start_datetime, end_datetime, description=''):
    """
    Creates a new event in the Google Calendar.
    
    Args:
        title (str): Event title
        start_datetime (datetime): Event start time (aware datetime)
        end_datetime (datetime): Event end time (aware datetime)
        description (str): Event description
    """
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


# Example usage:
if __name__ == "__main__":
    tz = pytz.timezone(TIMEZONE)
    start = datetime.now(tz) + timedelta(hours=1)
    end = start + timedelta(hours=2)
    event = create_event(
        title="Test Booking Event",
        start_datetime=start,
        end_datetime=end,
        description="This is a test booking event."
    )
    print(f"Event created: {event.get('htmlLink')}")
