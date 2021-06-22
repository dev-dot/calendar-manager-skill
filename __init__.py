

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



    @intent_file_handler('ask.next.appointment.specific.intent')
    def handle_ask_specific(self,message):

        date = message.data['date']
        

        start_date = extract_datetime(date)[0]
        end_date = datetime.combine(start_date,start_date.max.time())
        
        spoken_date = nice_date(start_date)

      
        calendar = self.get_calendars()[0]
        events = self.get_all_events(calendar= calendar, start= start_date.astimezone(pytz.timezone('Europe/Amsterdam')), end= end_date.astimezone(pytz.timezone('Europe/Amsterdam')))
        event_len = len(events)

        if (len(events)==0):
            self.speak_dialog('no.appointments.specific', {'date':spoken_date})
        elif(len(events)>=1):
            self.speak_dialog('yes.appointments.specific', {'number': event_len,'date':spoken_date})
            for event in events:
                next_event = event.instance.vevent
                start = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
                end = self.get_time_string(next_event.dtend.value)
                summary = next_event.summary.value

                self.log.info("Appointments found: %s",event_len)

                self.speak_dialog('yes.appointment.specific.all', {'title': summary, 'start': start, 'end':end})
              
        else: 
            self.speak(f"{date} is not a weekday. Please rephrase your question.")

    
    @intent_file_handler('ask.next.number.intent')
    def handle_ask_number(self,message):
        number_speak = message.data['number']
        
        number = extract_number(number_speak)
 
        calendar = self.get_calendars()[0]

        future_events = self.get_all_events(calendar=calendar, start=datetime.now().astimezone())

        if (len(future_events) == 0):
            self.speak_dialog('no.appointments.number')
        else:
            #future_events.sort(key=lambda event: event.instance.vevent.dtstart.value.astimezone())
            if number > len(future_events):
                self.speak("You dont have enough events")
            else:
                self.speak("Your following events are")
                for i in range(number):
                    self.log.info(future_events[i].instance.vevent)
                    next_event = future_events[i].instance.vevent
                    starttime = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
                    endtime = self.get_time_string(next_event.dtend.value)
                    summary = next_event.summary.value

                    start_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"
                    end_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"


                    self.speak_dialog('yes.appointments', {'title': summary, 'startdate': start_date_string, 'starttime': starttime, 'enddate':end_date_string, 'endtime':endtime})







        #TODO: Timezone - Events die Zurück kommen haben nicht die richtige Zeitzone | Die events die wir bekommen schon  Prio 3
        #TODO: Specific Date - Haben wir "morgen" ein Termin | "day after tomorrow" | Abfrage nach Datum  Prio 1 -> Done "Do i have an appointment on July first "
        #TODO: Bewusste Anzahl an Terminenen ausrufen - Prio 2
        #TODO: Fehlerbehandlung sobald "morgen abend" keine Termine mehr vorhanden sind
        #TODO: Bonusaufgaben Prio 4


            


def create_skill():
    return CalendarManager()