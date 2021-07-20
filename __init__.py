

from time import gmtime
import time #FIXME: Do we need it?
from mycroft import MycroftSkill, intent_file_handler, audio

from dateutil import relativedelta
from datetime import date, datetime, timedelta, tzinfo
import caldav
from caldav.objects import Calendar
import pytz 
from lingua_franca.parse import extract_datetime, normalize, extract_number
from lingua_franca.format import nice_date
from tzlocal import get_localzone
from caldav.lib.error import AuthorizationError

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
                self.speak(f"You are successfully connected to your calendar: {self.current_calendar.name}") 
            except AuthorizationError as authorizationError:
                self.log.error(authorizationError)
                self.speak("A connection to your calendar is currently not possible! Check your crendentials!")
            except Exception as exception:
                self.log.error(exception)
                self.speak("Unexpected error! Check Logs! Check URL!")

    def get_client(self, caldav_url, username, password):
            try: 
                client = caldav.DAVClient(url=caldav_url, username=username, password=password)

                return client                
            except Exception as exception:
                self.log.error(exception)
                self.speak("Wrong credentials for calendar access! Please check your Password and Username and your ical url!")
         


    def get_calendars(self):
        calendars = self.client.principal().calendars()
        return calendars


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


    def get_event_title(self, event):
        try:
            return event.summary.value
        except:
            return "without a title"


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


    # TODO: if the event is over multiple days the output is wrong -> only the start date and the start time are correct
    # the end date is missing and the end time is correct but it seems at it is on the same day as the start date
    # -> 2 outputs for short events and for events over multiple days
    # TODO: helper method to check wether an event is over multiple days and use in all handle methods, maybe also state the output here directly
    
    def helper_speak_event(self, event, is_handle_specific = False):
        start_date = event.dtstart.value
        end_date = event.dtend.value
        self.log.info(start_date)
        self.log.info(end_date)
        title = self.get_event_title(event)
        start_date_string = f"{self.get_ordinal_number(start_date.day)} of {event.dtstart.value.strftime('%B')}"

        try:
            end_date_string = f"{self.get_ordinal_number(end_date.day)} of {event.dtend.value.strftime('%B')}"
            # hier versuche die Zeit aufzulösen

            # 1. am gleichen Tag mit times
            # 2. multiple days -> with times -> 2. date fehlt
            starttime = self.get_time_string(start_date) # TODO: check if there is a try in get_time_string
            endtime = self.get_time_string(end_date)

            if start_date.day == end_date.day:
                self.speak_dialog('yes.same.day.appointment.with.times', {'title': title, 'startdate': start_date_string, 'starttime': starttime, 'endtime':endtime})

                if is_handle_specific:
                    self.speak_dialog('specific.yes.same.day.appointment.with.times')
            else:
                self.speak_dialog('yes.multiple.days.appointment.with.times', {'title': title, 'startdate': start_date_string, 'starttime': starttime, 'enddate':end_date_string, 'endtime':endtime})

        except:
        # 1. one whole day -> no times
        # 2. multiple days -> no times

            start_date_string = f"{self.get_ordinal_number(start_date.day)} of {event.dtstart.value.strftime('%B')}" 

            amount_of_days = date(end_date) - date(start_date)

            if amount_of_days.days - 1 == 0: # has to be one day less, because caldav counts till the follwing day at 0 o'clock
                # case one whole day & no times
                # TODO: add dialog
                self.speak_dialog('yes.appointment.all.day.same.day.dialog', {'title': title, 'startdate': start_date_string})
            else:
                # case multiple days & no times
                self.speak_dialog('yes.appointment.all.day.dialog', {'title': title, 'startdate': start_date_string, 'duration': amount_of_days.days})


    @intent_file_handler('ask.calendar.change.intent')
    def choose_calendar(self):
        calendar_names = list()
        
        for calendar in self.get_calendars():
            calendar_names.append(calendar.name)
        
        self.log.info(calendar_names)

        calendar_position = 0
        counter = 0
        self.speak('Choose from one of the following calendars by saying the number')
        selection = self.ask_selection(options=calendar_names, numeric=True)       
      
        for calendar in self.get_calendars():
            if calendar.name == selection:
                calendar_position = counter
            counter += 1

        if selection is not None:
            selected_calendar = self.get_calendars()[calendar_position]
            self.log.info(selected_calendar.name)
            self.log.info(calendar_position)
            self.speak(f"You chose {selected_calendar.name}")
            self.current_calendar = selected_calendar
        
        else:
            self.speak(f"Canceled selection. Your current calendar is {self.current_calendar.name}")


    @intent_file_handler('ask.next.appointment.intent')
    def handle_next_appointment(self):  
        
        calendar = self.current_calendar
        if calendar is None:
            self.speak('No calendar accessible')
            return

        future_events = self.get_all_events(calendar=calendar, start=datetime.now().astimezone())

        if len(future_events) == 0:
            self.speak_dialog('no.appointments')
        else:
            self.log.info(future_events[0].instance.vevent)
            next_event = future_events[0].instance.vevent
            self.helper_speak_event(next_event)


    @intent_file_handler('ask.next.appointment.specific.intent')
    def handle_ask_specific(self, message):

        date = message.data['date']

        try:
            start_date = extract_datetime(date)[0] 
            end_date = datetime.combine(start_date,start_date.max.time())
            calendar = self.current_calendar
            if calendar is None:
                self.speak('No calendar accessible')
                return
            events = self.get_all_events(calendar= calendar, start= start_date.astimezone(self.local_tz), end= end_date.astimezone(self.local_tz))
            spoken_date = nice_date(start_date)
            
            if len(events)==0:

                self.speak_dialog('no.appointments.specific', {'date':spoken_date})
                next_event = self.get_all_events(calendar= calendar, start= start_date.astimezone(self.local_tz)) # TODO: try to use next_appointment func
                if len(next_event) > 0:
                    
                    start_date_string = f"{self.get_ordinal_number(next_event[0].instance.vevent.dtstart.value.day)} of {next_event[0].instance.vevent.dtstart.value.strftime('%B')}"
                   
                    summary = self.get_event_title(next_event[0].instance.vevent)
                    self.speak_dialog('yes.next.appointment.specific', {'title': summary, 'date': start_date_string})
                    
            elif len(events)>=1:
                self.speak_dialog('yes.appointments.specific', {'number': len(events),'date':spoken_date})
                for event in events:
                    next_event = event.instance.vevent

                    start = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
                    end = self.get_time_string(next_event.dtend.value)
                    self.log.info(start)

                    self.log.info(next_event.dtstart.value)

                    summary = self.get_event_title(next_event)

                    self.log.info("Appointments found: %s",len(events))

                    self.speak_dialog('yes.appointment.specific.all', {'title': summary, 'start': start, 'end':end})
                
        except TypeError as typeError:
            self.log.error(typeError)
            self.speak(f"{date} is not a valid input. Please rephrase your question.")
        except Exception as exception:
            self.log.error(exception)
            self.speak("Unexpected error! Check Logs!")  


    @intent_file_handler('ask.next.number.intent')
    def handle_ask_number(self,message):
        number_speak = message.data['number']
        
        number = extract_number(number_speak)
 
        calendar = self.current_calendar
        if calendar is None:
            self.speak('No calendar accessible')
            return

        future_events = self.get_all_events(calendar=calendar, start=datetime.now().astimezone())
   
        if len(future_events) == 0:
            self.speak_dialog('no.appointments.number')
        else:
            if number > len(future_events):
                self.speak(f"You have only {len(future_events)} upcoming events and they are")
                number = len(future_events)
            else:
                self.speak("Your following events are")    
        
            for i in range(number):
                audio.wait_while_speaking()
                self.log.info(future_events[i].instance.vevent)
                next_event = future_events[i].instance.vevent
                starttime = self.get_time_string(next_event.dtstart.value) #TODO: add Duration
                endtime = self.get_time_string(next_event.dtend.value)
                summary = self.get_event_title(next_event)
                start_date_string = f"{self.get_ordinal_number(next_event.dtstart.value.day)} of {next_event.dtstart.value.strftime('%B')}"
                end_date_string = f"{self.get_ordinal_number(next_event.dtend.value.day)} of {next_event.dtend.value.strftime('%B')}"

                self.speak_dialog('yes.appointments', {'title': summary, 'startdate': start_date_string, 'starttime': starttime, 'enddate':end_date_string, 'endtime':endtime})



# Bonus "DELETE"

'''
    @intent_file_handler('ask.delete.event.intent')
    def delete_events(self,message):

        date = message.data['date']
       
        start_date = extract_datetime(date)[0] 
        end_date = datetime.combine(start_date,start_date.max.time())
        calendar = self.current_calendar
        if calendar is None:
            self.speak('No calendar accessible')
            return
        events = self.get_all_events(calendar= calendar, start= start_date.astimezone(self.local_tz), end= end_date.astimezone(self.local_tz))
        spoken_date = nice_date(start_date)
        
        if len(events) == 0:
            self.speak_dialog('no.appointments')
        elif len(events) == 1:
            next_event = events[0].instance.vevent
            summary = self.get_event_title(next_event

            shall_be_deleted = self.ask_yesno(f"Do you want to delete this appointment {summary}?")
            if shall_be_deleted == 'yes':
                # TODO: try deletion
                self.speak_dialog('successfully deleted')
                delete_specific_event(next_event)
            elif shall_be_deleted == 'no':
                self.speak_dialog('Canceled deletetion')
            else:
                self.speak_dialog('I could not understand you.') # TODO: is this really neccesary?
            # ask if the user wants to delete a specific event
        
        else:
            event_names = list()
        
            for event in events:
                next_event = event.instance.vevent
                summary = self.get_event_title(next_event)

                event_names.append(summary)
            
            event_position = 0
            counter = 0
            self.speak_dialog('Which of the following events do you want to delete?')
            selection = self.ask_selection(options=event_names, numeric= True)
            
            for event in events:
                next_event = event.instance.vevent
                summary = self.get_event_title(next_event)

                if summary == selection:
                    event_position = counter
                counter += 1

            if selection is not None:
                selected_event = events[event_position]
                self.speak(f"You chose {selected_event.name}")
                # delete specific
            
            else:
                self.speak(f"Cancled selection.")

        def delete_specific_event(self, event):
            try:
                event.delete()
            except:
                self.speak('An error occured and thus selected event could not be deleted')
'''

        #TODO: Fehlerbehandlung sobald "morgen abend" keine Termine mehr vorhanden sind
        #TODO: handle if summary is empty -> summary key is missing
        #TODO: Dokumentation
        #TODO: Applikation Crasht bei einem ganztäglichen termin und zeigt das falsche Datum bei einem mehrtagigen termin
                # Bei ganztägigen Terminen wird keine Timezone mitgegeben -> es gibt für DTSTART keine Uhrzeit in ms sondern ein datum 
                # Problem taucht beim end_date auf -> das Enddate bei mehrtägigen Terminen ist das selbe im Output wie das Startdate, lediglich die endtime ist richtig
        #TODO: Errorhandling
        #TODO: Code verschönern
        #TODO: Code nach richtline Kommentieren 

        #TODO: Bonusaufgaben             


def create_skill():
    return CalendarManager()