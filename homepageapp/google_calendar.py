import os
import json
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build

CALENDAR_ID = "restaurantbookingproject@restaurant-booking-calendar.iam.gserviceaccount.com"
TIMEZONE = "Europe/London"

service = None

raw_creds = os.environ.get("GOOGLE_CREDS")

if raw_creds:
	try:
		# Try decode as base64 first
		try:
			decoded = base64.b64decode(raw_creds).decode("utf-8")
			creds_data = json.loads(decoded)
		except Exception:
			# If decoding fails, assume it's already JSON
			creds_data = json.loads(raw_creds)

		credentials = service_account.Credentials.from_service_account_info(
			creds_data,
			scopes=["https://www.googleapis.com/auth/calendar"],
		)

		service = build("calendar", "v3", credentials=credentials)
		print("✅ Google Calendar connected successfully.")

	except Exception as e:
		print(f"⚠️ Google Calendar Setup Error: {e}")
else:
	print("⚠️ GOOGLE_CREDS environment variable not found.")


def create_event(title, start_datetime, end_datetime, description=""):
	"""
	Creates an event in Google Calendar safely (won't crash the site).
	"""
	if not service:
		print("⚠️ Google Calendar service not available.")
		return None

	event_data = {
		"summary": title,
		"description": description,
		"start": {
			"dateTime": start_datetime.isoformat(),
			"timeZone": TIMEZONE,
		},
		"end": {
			"dateTime": end_datetime.isoformat(),
			"timeZone": TIMEZONE,
		},
	}

	try:
		event = service.events().insert(calendarId=CALENDAR_ID, body=event_data).execute()
		return event
	except Exception as e:
		print("⚠️ Calendar Event Creation Error:", e)
		return None