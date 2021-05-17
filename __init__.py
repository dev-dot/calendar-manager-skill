
from mycroft import MycroftSkill, intent_file_handler


from datetime import datetime
import caldav
from caldav.objects import Calendar
import regex
import icalendar 
import pytz 

Utc = pytz.UTC
class CalendarManager(MycroftSkill):
    


    def __init__(self):
        MycroftSkill.__init__(self)
      #  self.local_timezone = local_timezone
        self.caldav_url = 'https://si-nextcloud.social-robot.info/remote.php/dav'
        self.username = 'ar140@hdm-stuttgart.de'
        self.password = 'Mycroftgruppe5'
        self.client = caldav.DAVClient(url=self.caldav_url, username=self.username, password=self.password)
        self.the_same_calendar = self.client.calendar(url="https://si-nextcloud.social-robot.info/remote.php/dav/calendars/ar140%40hdm-stuttgart.de/personal/")
        

    def get_calendars(self):
        principal = self.client.principal()
        calendars = principal.calendars()
        
        return calendars

    def whats_my_next_appointment(self, calendar: Calendar):
        all_events = calendar.events()
        parse_next_event = self.parse_ics_events(all_events)
      
        print(parse_next_event[0])
        return parse_next_event[0]


    def get_event_details(self, event):
        title = "untitled event"
        if "SUMMARY" in event.keys():
            title = str(event["SUMMARY"])

        return {"title": title} 

    def parse_ics_events(self, events):
        
        parsed_events = []
        for event in events:
            cal = icalendar.Calendar.from_ical(event.data, True)
            url = event.url
            for vevent in cal[0].walk("vevent"):
                event_details = self.get_event_details(vevent)
                event_details["event_url"] = url
                parsed_events.append(event_details)
        return parsed_events


    @intent_file_handler('ask.next.appointment.intent')
    def handle_manager_calendar(self, message):
        next_appointment = self.whats_my_next_appointment(self.the_same_calendar)
        #title = ' '.join(regex.search("SUMMARY:.*?:", next_appointment, regex.DOTALL).group().replace(':', ' ').split()[1:-1])
        
        self.speak_dialog('next.appointment', {'title': next_appointment['title']})

def create_skill():
    return CalendarManager()
