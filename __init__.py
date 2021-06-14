

from time import gmtime
import time
from mycroft import MycroftSkill, intent_file_handler

from dateutil import relativedelta
from datetime import date, datetime, timedelta, tzinfo
import caldav
from caldav.objects import Calendar
import icalendar 
import pytz 



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

    #def whats_my_next_appointment(self, calendar: Calendar):
      #  currentDate = datetime.today()

    #    all_future_events = calendar.date_search(start=datetime(currentDate.year,currentDate.month,currentDate.day),end=datetime(currentDate.year+1,currentDate.month,currentDate.day),expand=True)
     #   parse_next_event = self.parse_ics_events(all_future_events)
    #    all_events = self.get_all_events(calendar, datetime.now())  
        # print(parse_next_event[0])
      #  print(all_events[0].data)
       # return parse_next_event[0]

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
            all_events.sort(key=lambda event: event.instance.vevent.dtstart.value.astimezone())     
            return all_events


        


    def get_event_details(self, event):
        title = "untitled event"
        if "SUMMARY" in event.keys():
            title = str(event["SUMMARY"])

       # event_start = "not choosed"    
       # if "DTSTART" in event.key():
       #     event_start = str(event["DTSTART"])

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

    def get_time_string(self, vevent_date: datetime, with_time: bool = True):
        time_string = f" at {vevent_date.strftime('%H:%M')}"
        return time_string


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
    
    def get_ordinal_number(self,i):
        switcher={
            1: 'first',
            2: 'second',
            3: 'third',
            4: 'fourth',
            5: 'fifth',
            6:  'sixth',
            7:  'seventh',
            8:  'eighth',
            9:  'ninth',
            10: 'tenth',
            11: 'eleventh',
            12: 'twelfth',
            13: 'thirteenth',
            14: 'fourteenth',
            15: 'fifteenth',
            16: 'sixteenth',
            17: 'seventeenth',
            18: 'eighteenth',
            19: 'nineteenth',
            20: 'twentieth',
            21: 'twenty-first',
            22: 'twenty-second',
            23: 'twenty-third',
            24: 'twenty-fourth',
            25: 'twenty-fifth',
            26: 'twenty-sixth',
            27: 'twenty-seventh',
            28: 'twenty-eighth',
            29: 'twenty-ninth',
            30: 'thirtieth',
            31: 'thirty-first'
            }
        return switcher.get(i,"Invalid day of the month")

    @intent_file_handler('ask.next.appointment.intent')
    def handle_next_appointment(self, message):
        
        calendar = self.get_calendars()[0]

        future_events = self.get_all_events(calendar=calendar, start=datetime.now().astimezone())

        if (len(future_events) == 0):
            self.speak_dialog('no.appointments')
        else:
            #future_events.sort(key=lambda event: event.instance.vevent.dtstart.value.astimezone())
            self.log.info(future_events[0].instance.vevent)
            next_event = future_events[0].instance.vevent
            starttime = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
            endtime = self.get_time_string(next_event.dtend.value)
            summary = next_event.summary.value

            start_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"
            end_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"


            self.speak_dialog('next.appointment', {'title': summary, 'startdate': start_date_string, 'starttime': starttime, 'enddate':end_date_string, 'endtime':endtime})

    @intent_file_handler('ask.next.appointment.weekday.intent')
    def handle_ask_weekday(self,message):

        weekday = message.data['weekday']

        event_date = self.search_date_from_weekday(self.parse_weekday(weekday))

        if (self.parse_weekday(weekday) == event_date.today().weekday()):
            event_date = event_date + timedelta(days=7)
            print(self.parse_weekday(weekday))
            print(event_date.today().weekday())
        else:
            event_date = event_date + timedelta(days=0)
            print(self.parse_weekday(weekday))
            print(event_date.today().weekday())

        event_date_string = f"{self.get_ordinal_number(event_date.day)} of {event_date.strftime('%B')}"
        start_search = datetime.combine(event_date,datetime.min.time())
        date_end = date(event_date.year,event_date.month,event_date.day+1)
        end_search = datetime.combine(date_end, datetime.min.time())
  
        calendar = self.get_calendars()[0]
        events = self.get_all_events(calendar= calendar, start= start_search, end= end_search)
        event_len = len(events)

        if (len(events)==0):
            self.speak_dialog('no.appointments.weekday', {'weekday':weekday, 'date':event_date_string})
        elif(len(events)>=1):
            self.speak_dialog('yes.appointments.weekday', {'number': event_len,'weekday':weekday, 'date':event_date_string})
            for event in events:
                next_event = event.instance.vevent
                start = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
                end = self.get_time_string(next_event.dtend.value)
                summary = next_event.summary.value
                
                self.log.info("Appointments found: %s",event_len)
                
                self.speak_dialog('yes.appointment.weekday.first', {'title': summary, 'start': start, 'end':end})

               

       # self.speak(weekday)
        self.log.info("Start date: %s", start_search)
        self.log.info("End Date: %s", end_search)

    
        #TODO: Timezone 
        #TODO: Specific Date 
        #TODO: Bewusste Anzahl an Terminenen ausrufen 
        #TODO: Bonusaufgaben

def create_skill():
    return CalendarManager()