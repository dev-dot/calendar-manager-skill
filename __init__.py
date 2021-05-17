
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
        next_event_details = self.get_event_details(parse_next_event[0]) #ToDO change names
        return next_event_details


    def get_event_details(self, event):
        
        start = None
       # if "DTSTART" in event.keys():
         #   start = event["DTSTART"].dt
         #   if not isinstance(start, datetime):
          #      start = datetime.combine(start, datetime.min.time())
         #       start = start.replace(tzinfo=Utc)
        #    else:
       #         start = start.astimezone(self.local_timezone)
      #  end = None
      #  if "DTEND" in event.keys():
       #     end = event["DTEND"].dt
        #    if not isinstance(end, datetime):
         #       end = datetime.combine(end, datetime.min.time())
          #      end = end.replace(tzinfo=Utc)
           # else:
            #    end = end.astimezone(self.local_timezone)
        title = "untitled event"
        if "SUMMARY" in event.keys():
            title = str(event["SUMMARY"])

        return {"title": title} #"starttime": start, "endtime": end

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
