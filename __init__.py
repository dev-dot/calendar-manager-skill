

from icalendar import cal
from mycroft import MycroftSkill, intent_file_handler

from dateutil import relativedelta
from datetime import date, datetime, timedelta
import caldav
from caldav.objects import Calendar
import icalendar 
import pytz 
import vobject
import calendar as calendarday


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

        all_future_events = calendar.date_search(start=datetime(currentDate.year,currentDate.month,currentDate.day),end=datetime(currentDate.year+1,currentDate.month,currentDate.day),expand=True)
        parse_next_event = self.parse_ics_events(all_future_events)
        all_events = self.get_all_events(calendar, datetime.now())  
        # print(parse_next_event[0])
        print(all_events[0].data)
        return parse_next_event[0]

    #def filter_events(self, events):

    #    for event in events:
      #      if "DTSTART":
          

    def get_event_data_string(self, event):
        starttime = event.instance.vevent.dtstart.value
        print(starttime)


    def get_all_events(self, calendar: Calendar, start: datetime = None, end: datetime = None):
        
        all_events = []

        if start is None:
            return calendar.events()
        else:
            event_date = calendar.date_search(start=start, end=end)
            

            for event in event_date:
                event_start = event.instance.vevent.dtstart.value

                # for all day events
                if not isinstance(event_start, datetime):
                    event.instance.vevent.dtstart.value = datetime.combine(event_start, datetime.min.time())

                if event.instance.vevent.dtstart.value.astimezone() >= start.astimezone():
                    all_events.append(event)
            if end is not None:
                all_events = [i for i in all_events if 
                 i.instance.vevent.dtstart.value.astimezone() <= end.astimezone()] 
            return all_events


        


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


    def date_to_string(self, vevent_date: datetime, with_time: bool =True):
   
        date_string = f"{vevent_date.strftime('%B')} {vevent_date.strftime('%d')}, {vevent_date.strftime('%Y')}"
        if with_time:
            date_string = date_string + f" at {vevent_date.strftime('%H:%M')}"
        return date_string

    def parse_weekday(self,i):
        switcher={
                'monday'    : 0,
                'tuesday'   : 1,
                'wednesday' : 2,
                'thurday'   : 3,
                'friday'    : 4,
                'saturday'  : 5,
                'sunday'    : 6
             }
        return switcher.get(i,"Invalid day of week")

    def search_date_from_weekday(self, weekday_int):
        today = date.today()
        next_date = today + relativedelta.relativedelta(weekday= weekday_int)
        return next_date
    


    @intent_file_handler('ask.next.appointment.intent')
    def handle_next_appointment(self, message):
        
        calendar = self.get_calendars()[0]

        future_events = self.get_all_events(calendar=calendar, start=datetime.now().astimezone())

        if (len(future_events) == 0):
            self.speak_dialog('no.appointments')
        else:
            future_events.sort(key=lambda event: event.instance.vevent.dtstart.value.astimezone())

            next_event = future_events[0].instance.vevent
            start = self.date_to_string(next_event.dtstart.value) #TODO: add Duration
            end = self.date_to_string(next_event.dtend.value)
            summary = next_event.summary.value

            
            self.speak_dialog('next.appointment', {'title': summary, 'start': start, 'end':end})

    @intent_file_handler('ask.next.appointment.weekday.intent')
    def handle_ask_weekday(self,message):

        weekday = message.data['weekday']
        date = self.search_date_from_weekday(self.parse_weekday(weekday))
        start = datetime.combine(date,datetime.min.time())
        date_end = date(start.year,start.month,start.day+1)
        end = datetime.combine(date_end, datetime.min.time())

        calendar = self.get_calendars()[0]
        events = self.get_all_events(calendar= calendar, start= start, end= end)

        if (len(events)==0):
            self.speak("you have no appointment on ", weekday)

        print(start)
        print(end)
        self.speak(weekday)
        self.log.info("Test start:", start)
        self.log.info("Test end:", end)
     

def create_skill():
    return CalendarManager()