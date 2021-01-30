from __future__ import print_function
import datetime
import pickle
import os.path
from datetime import datetime
import calendar
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from mycroft import MycroftSkill, intent_file_handler

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def googleCalendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming event')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    return events


def getLocationData():

    events = googleCalendar()

    locationData = ''
    for event in events:
        try:
            locationData = event['location']
        except:
            print('There is no location set for this event.')

    return locationData


def getEventData():

    events = googleCalendar()

    eventData = ''
    for event in events:
        start = event['start'].get('dateTime')

        try:
            eventData = start, event['summary']
        except:
            print('There is no upcoming event.')

    (eventDayTime, eventName) = eventData
    timeObject = datetime.strptime(eventDayTime, '%Y-%m-%dT%H:%M:%S%z')
    eventTime = (timeObject.time()).strftime("%H:%M:%S")
    eventDay = calendar.day_name[(timeObject.date().isoweekday())-1]

    CalendarDataDict = {
        'meetingResult': eventName,
        'dayResult': eventDay,
        'timeResult': eventTime
    }

    return CalendarDataDict


class GoogleCalendar(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('calendar.google.intent')
    def handle_calendar_google(self, message):
        eventDataDict = getEventData()
        self.speak_dialog('calendar.google', eventDataDict)


def create_skill():
    return GoogleCalendar()
