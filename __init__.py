

from time import gmtime
import time
from mycroft import MycroftSkill, intent_file_handler

from dateutil import relativedelta
from datetime import date, datetime, timedelta, tzinfo
import caldav
from caldav.objects import Calendar
import icalendar 
import pytz 
from lingua_franca.parse import extract_datetime, normalize, extract_number
from lingua_franca.format import nice_date
from tzlocal import get_localzone



class CalendarManager(MycroftSkill):



    def __init__(self):
        super().__init__()
        self.current_calendar = None
      # self.local_tz = pytz.timezone('Europe/Berlin')
        self.local_tz = get_localzone() 

    def initialize(self): 
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()

    def on_settings_changed(self):
        caldav_url = self.settings.get('ical_url')
        username = self.settings.get('username')
        password = self.settings.get('password')
        self.client = self.get_client(caldav_url, username, password) 
        if self.client is not None:
            try: 
                self.current_calendar = self.get_calendars()[0]
                self.speak("You are successfully connected to your calendar")
            except:
                self.speak("Wrong credentials for calendar access! Please check your Password and Username and your ical url!")
        
    def get_client(self, caldav_url, username, password):
            try: 
                client = caldav.DAVClient(url=caldav_url, username=username, password=password)

                return client                
            except:
                self.speak("Wrong credentials for calendar access! Please check your Password and Username and your ical url!")
                

    def get_calendars(self):
        calendars = self.client.principal().calendars()
        return calendars

    @intent_file_handler('ask.calendar.change.intent')
    def choose_calendar(self):
        calendar_names = list()
        
        for calendar in self.get_calendars():
            calendar_names.append(calendar.name)
        
        self.log.info(calendar_names)

       
        calendar_position = 0
        counter = 0
        selection =  self.ask_selection(options=calendar_names, dialog='Choose your calendar by saying only the Number!', numeric= True)
       
      
        for calendar in self.get_calendars():
            if calendar.name == selection:
                calendar_position = counter
            counter += 1

        selected_calendar = self.get_calendars()[calendar_position]
        
        self.log.info(selected_calendar.name)
        self.log.info(calendar_position)
        self.speak(f"You chose {selected_calendar.name}")
        self.current_calendar = selected_calendar
       

    


    def get_event_data_string(self, event):
        starttime = event.instance.vevent.dtstart.value
        self.log.info(starttime)


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

                if event.instance.vevent.dtstart.value.astimezone(self.local_tz) >= start.astimezone(self.local_tz):
                    all_events.append(event)
            if end is not None:
                all_events = [i for i in all_events if
                 i.instance.vevent.dtstart.value.astimezone(self.local_tz) <= end.astimezone(self.local_tz)]
            all_events.sort(key=lambda event: event.instance.vevent.dtstart.value.astimezone(self.local_tz))
            return all_events



        

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


    def date_to_string(self, vevent_date: datetime, with_time: bool =True):
        #vevent_date
        date_string = f"{vevent_date.strftime('%B')} {vevent_date.strftime('%d')}, {vevent_date.strftime('%Y')}"
        if with_time:
            date_string = date_string + f" at {vevent_date.strftime('%H:%M')}"
        return date_string

    def get_time_string(self, vevent_date: datetime, with_time: bool = True):
       # vevent_date
        time_string = f" {vevent_date.astimezone(self.local_tz).strftime('%H:%M')}"
        self.log.info(time_string)
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
        
        calendar = self.current_calendar
        future_events = self.get_all_events(calendar=calendar, start=datetime.now().astimezone())

        if (len(future_events) == 0):
            self.speak_dialog('no.appointments')
        else:
            self.log.info(future_events[0].instance.vevent)
            next_event = future_events[0].instance.vevent
            starttime = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
            endtime = self.get_time_string(next_event.dtend.value)
            summary = next_event.summary.value

            start_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"
            end_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"


            self.speak_dialog('next.appointment', {'title': summary, 'startdate': start_date_string, 'starttime': starttime, 'enddate':end_date_string, 'endtime':endtime})



    @intent_file_handler('ask.next.appointment.specific.intent')
    def handle_ask_specific(self,message):

        date = message.data['date']

        local_tz = pytz.timezone('Europe/Berlin')
       
        start_date = extract_datetime(date)[0] # fehler 
        end_date = datetime.combine(start_date,start_date.max.time())
        
        spoken_date = nice_date(start_date)

      
        calendar = self.current_calendar
        events = self.get_all_events(calendar= calendar, start= start_date.astimezone(local_tz), end= end_date.astimezone(local_tz))
        event_len = len(events)

        if len(events)==0:

            self.speak_dialog('no.appointments.specific', {'date':spoken_date})
            next_event = self.get_all_events(calendar= calendar, start= start_date.astimezone(local_tz))[0].instance.vevent
            if len(next_event) > 0:
                
                start_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"
                summary = next_event.summary.value
                self.speak_dialog('yes.next.appointment.specific', {'title': summary, 'date': start_date_string})
            
        elif len(events)>=1:
            self.speak_dialog('yes.appointments.specific', {'number': event_len,'date':spoken_date})
            for event in events:
                next_event = event.instance.vevent

                start = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
                end = self.get_time_string(next_event.dtend.value)
                self.log.info(start)

                self.log.info(next_event.dtstart.value)

                summary = next_event.summary.value

                self.log.info("Appointments found: %s",event_len)

                self.speak_dialog('yes.appointment.specific.all', {'title': summary, 'start': start, 'end':end})
              
        else: 
            self.speak(f"{date} is not a weekday. Please rephrase your question.")

    
    @intent_file_handler('ask.next.number.intent')
    def handle_ask_number(self,message):
        number_speak = message.data['number']
        
        number = extract_number(number_speak)
 
        calendar = self.current_calendar

        future_events = self.get_all_events(calendar=calendar, start=datetime.now().astimezone())
   
        if (len(future_events) == 0):
            self.speak_dialog('no.appointments.number')
        else:
         
            if number > len(future_events):
                self.speak(f"You have only {len(future_events)} upcoming events")

            self.speak("Your following events are")
            for i in range(len(future_events)):
                self.log.info(future_events[i].instance.vevent)
                next_event = future_events[i].instance.vevent
                starttime = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
                endtime = self.get_time_string(next_event.dtend.value)
                summary = next_event.summary.value

                start_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"
                end_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"



                self.speak_dialog('yes.appointments', {'title': summary, 'startdate': start_date_string, 'starttime': starttime, 'enddate':end_date_string, 'endtime':endtime})







        #TODO: Timezone - Events die Zurück kommen haben nicht die richtige Zeitzone | Die events die wir bekommen schon  Prio 3 -> DONE
        #TODO: Specific Date - Haben wir "morgen" ein Termin | "day after tomorrow" | Abfrage nach Datum  Prio 1 -> Done "Do i have an appointment on July first "
        #TODO: Bewusste Anzahl an Terminenen ausrufen - Prio 2
        #TODO: Fehlerbehandlung sobald "morgen abend" keine Termine mehr vorhanden sind
        
        
        #TODO: LogIn Errorhandling -> done
        #TODO: Bonusaufgaben 
        #TODO: Dokumentation
        #TODO: Code verschönern
        #TODO: Code nach richtline Kommentieren 


            


def create_skill():
    return CalendarManager()