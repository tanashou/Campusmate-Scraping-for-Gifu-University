import os.path
import os
from urllib.error import HTTPError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CALENDAR_ID = os.getenv("GIFU_UNI_SCRAPER_CAL_ID")


def add_events_to_calendar(events_list):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        for event in events_list:
            event_info = {"summary": f"{event.event_text}"}
            # event_info['location'] = f'{event.location}'
            # event_info['description'] = f'{event.location}'

            if event.is_one_day_event:
                event_info["start"] = {"date": f"{event.start_date_time.date()}", "timeZone": "Asia/Tokyo"}
                event_info["end"] = {"date": f"{event.end_date_time.date()}", 'timeZone': 'Asia/Tokyo'}

            else:
                event_info["start"] = {"dateTime": f"{event.start_date_time}", "timeZone": "Asia/Tokyo"}
                event_info["end"] = {"dateTime": f"{event.end_date_time}", 'timeZone': 'Asia/Tokyo'}

            insertingEvent = service.events().insert(calendarId=CALENDAR_ID, body=event_info).execute()
            print(f"Event created: %s" % (insertingEvent.get("summary")))

    except HTTPError as error:
        print("An error occurred: %s" % error)
