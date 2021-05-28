
from icalendar import cal
from mycroft import MycroftSkill, intent_file_handler


from datetime import date, datetime
import caldav
from caldav.objects import Calendar
import icalendar 
import pytz 
import vobject

Utc = pytz.UTC
class CalendarManager(MycroftSkill):
    


    def __init__(self):
        MycroftSkill.__init__(self)
      #  self.local_timezone = local_timezone
        self.caldav_url = self.settings.get('ical_url')
        self.username = self.settings.get('username')
        self.password = self.settings.get('password')
        self.client = caldav.DAVClient(url=self.caldav_url, username=self.username, password=self.password)
        self.the_same_calendar = self.client.calendar(url = self.get_calendars()[0].url)
        

    def get_calendars(self):
        principal = self.client.principal()
        calendars = principal.calendars()
        self.log.info(calendars)
        return calendars

    def whats_my_next_appointment(self, calendar: Calendar):
        currentDate = datetime.today()

        all_events = calendar.date_search(start=datetime(currentDate.year,currentDate.month,currentDate.day),end=datetime(currentDate.year+1,currentDate.month,currentDate.day),expand=True)
        parse_next_event = self.parse_ics_events(all_events)
        print(parse_next_event[0])
        self.get_event_data_string(all_events[0])
        return parse_next_event[0]

    #def filter_events(self, events):

    #    for event in events:
      #      if "DTSTART":
          

    def get_event_data_string(self, event):
        starttime = cal.vevent.dtstart.valueRepr()
        print(starttime)

    def get_event_details(self, event):
        title = "untitled event"
        if "SUMMARY" in event.keys():
            title = str(event["SUMMARY"])

       # event_start = "not choosed"    
       # if "DTSTART" in event.key():
        #    event_start = str(event["DTSTART"])

        #event_end = None     
        #if "DTEND" in event.keys():
        #    event_end = str(event["DTEND"]) '

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
       
        self.speak_dialog('next.appointment', {'title': next_appointment['title']})

def create_skill():
    return CalendarManager()