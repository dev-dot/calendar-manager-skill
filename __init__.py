from time import gmtime
import time
from datetime import date, datetime, timedelta, tzinfo
from mycroft import MycroftSkill, intent_file_handler, audio

from dateutil import relativedelta

import caldav
from caldav.objects import Calendar
import pytz
from lingua_franca.parse import extract_datetime, normalize, extract_number
from lingua_franca.format import nice_date
from tzlocal import get_localzone
from caldav.lib.error import AuthorizationError

class CalendarManager(MycroftSkill):
    """[summary]

    Args:
        MycroftSkill ([type]): [description]
    """
    def __init__(self):
        """[summary]
        """
        super().__init__()
        self.current_calendar = None
      # self.local_tz = pytz.timezone('Europe/Berlin')
        self.local_tz = get_localzone()


    def initialize(self):
        """[summary]
        """
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()


    def on_settings_changed(self):
        """[summary]
        """
        caldav_url = self.settings.get('ical_url')
        username = self.settings.get('username')
        password = self.settings.get('password')
        self.client = self.get_client(caldav_url, username, password)
        if self.client is not None:
            try:
                self.current_calendar = self.get_calendars()[0]
                self.speak(f"You are successfully connected to your calendar: {self.current_calendar.name}")
            except AuthorizationError as authorization_error:
                self.log.error(authorization_error)
                self.speak("A connection to your calendar is currently not possible! Check your crendentials!")
            except Exception as exception:
                self.log.error(exception)
                self.speak("Unexpected error! Check Logs! Check URL!")


    def get_client(self, caldav_url, username, password):
        """[summary]

        Args:
            caldav_url ([type]): [description]
            username ([type]): [description]
            password ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            client = caldav.DAVClient(url=caldav_url, username=username, password=password)

            return client
        except Exception as exception:
            self.log.error(exception)
            self.speak("Wrong credentials for calendar access! Please check your Password and Username and your ical url!")
            return


    def get_calendars(self):
        calendars = self.client.principal().calendars()
        return calendars


    def get_all_events(self, calendar: Calendar, start: datetime = None, end: datetime = None):
        """[summary]

        Args:
            calendar (Calendar): [description]
            start (datetime, optional): [description]. Defaults to None.
            end (datetime, optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
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


    def get_event_title(self,event):
        """[summary]

        Args:
            event ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            return event.summary.value
        except:
            return "without a title"


    def date_to_string(self,vevent_date: datetime, with_time: bool =True):
        """[summary]

        Args:
            vevent_date (datetime): [description]
            with_time (bool, optional): [description]. Defaults to True.

        Returns:
            [type]: [description]
        """
        #vevent_date
        date_string = f"{vevent_date.strftime('%B')} {vevent_date.strftime('%d')}, {vevent_date.strftime('%Y')}"
        if with_time: date_string = date_string + f" at {vevent_date.strftime('%H:%M')}"
        return date_string


    def get_time_string(self, vevent_date: datetime):
        """[summary]

        Args:
            vevent_date (datetime): [description]

        Returns:
            [type]: [description]
        """

        try:
            time_string = f"{vevent_date.astimezone(self.local_tz).strftime('%H:%M')}"
            return time_string
        except:
            return None


    def get_ordinal_number(self,i):
        """[summary]

        Args:
            i ([type]): [description]

        Returns:
            [type]: [description]
        """
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



    def helper_speak_event(self, event, is_handle_specific = False):
        """[summary]

        Args:
            event ([type]): [description]
            is_handle_specific (bool, optional): [description]. Defaults to False.
        """
        audio.wait_while_speaking()

        start_date = event.dtstart.value
        end_date = event.dtend.value

        title = self.get_event_title(event)
        start_date_string = f"{self.get_ordinal_number(start_date.day)} of {event.dtstart.value.strftime('%B')}"

        starttime = self.get_time_string(start_date)
        endtime = self.get_time_string(end_date)

        if starttime is not None and endtime is not None:

            end_date_string = f"{self.get_ordinal_number(end_date.day)} of {event.dtend.value.strftime('%B')}"

            if start_date.day == end_date.day:
                self.speak_dialog('yes.same.day.appointment.with.times', {'title': title, 'startdate': start_date_string, 'starttime': starttime, 'endtime':endtime})

                if is_handle_specific:
                    self.speak_dialog('specific.yes.same.day.appointment.with.times')
            else:
                self.speak_dialog('yes.multiple.days.appointment.with.times', {'title': title, 'startdate': start_date_string, 'starttime': starttime, 'enddate': end_date_string, 'endtime' : endtime })

        else:
            # For all day events
            start_date_string = f"{self.get_ordinal_number(start_date.day)} of {event.dtstart.value.strftime('%B')}"

            amount_of_days = date(end_date.year, end_date.month, end_date.day) - date(start_date.year,start_date.month, start_date.day)

            if amount_of_days.days - 1 == 0: # has to be one day less, because caldav counts till the follwing day at 0 o'clock
                # case one whole day & no times
                self.speak_dialog('yes.appointment.same.day.all.day',{'title': title,'startdate': start_date_string})
            else:
                # case multiple days & no times
                self.speak_dialog('yes.appointment.all.day',
                {'title': title,
                 'startdate': start_date_string,
                 'duration': amount_of_days.days})


    @intent_file_handler('ask.calendar.change.intent')
    def choose_calendar(self):
        """[summary]
        """
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
        """[summary]
        """
        calendar = self.current_calendar
        if calendar is None:
            self.speak('No calendar accessible')
            return

        start_date = datetime.now().astimezone()

        future_events = self.get_all_events(calendar=calendar, start=start_date)

        if len(future_events) == 0:
            self.speak_dialog('no.appointments')
        else:
            self.log.info(future_events[0].instance.vevent)
            next_event = future_events[0].instance.vevent
            self.helper_speak_event(next_event)


    @intent_file_handler('ask.next.appointment.specific.intent')
    def handle_ask_specific(self, message):
        """[summary]

        Args:
            message ([type]): [description]
        """
        date = message.data['date']

        try:
            start_date = extract_datetime(date)[0]
            end_date = datetime.combine(start_date,start_date.max.time())
            calendar = self.current_calendar
            if calendar is None:
                self.speak('No calendar accessible')
                return
            events = self.get_all_events(calendar= calendar,
             start= start_date.astimezone(self.local_tz),
             end= end_date.astimezone(self.local_tz))
            spoken_date = nice_date(start_date)

            if len(events)==0:

                self.speak_dialog('no.appointments.specific', {'date':spoken_date})
                next_event = self.get_all_events(calendar= calendar, start= start_date.astimezone(self.local_tz))
                if len(next_event) > 0:

                    start_date_string = f"{self.get_ordinal_number(next_event[0].instance.vevent.dtstart.value.day)} of {next_event[0].instance.vevent.dtstart.value.strftime('%B')}"

                    summary = self.get_event_title(next_event[0].instance.vevent)

                    self.speak_dialog('yes.next.appointment.specific', {'title': summary,
                     'date': start_date_string})


            elif len(events)>=1:
                self.speak_dialog('yes.appointments.specific', {'number': len(events),'date':spoken_date})
                for event in events:
                    next_event = event.instance.vevent

                    self.helper_speak_event(next_event)

        except TypeError as type_error:
            self.log.error(type_error)
            self.speak(f"{date} is not a valid input. Please rephrase your question.")
        except Exception as exception:
            self.log.error(exception)
            self.speak("Unexpected error! Check Logs!")


    @intent_file_handler('ask.next.number.intent')
    def handle_ask_number(self,message):
        """[summary]

        Args:
            message ([type]): [description]
        """
        number_speak = message.data['number']

        number = extract_number(number_speak)

        calendar = self.current_calendar
        if calendar is None:
            self.speak('No calendar accessible')
            return

        future_events=self.get_all_events(calendar=calendar, start=datetime.now().astimezone())

        if len(future_events) == 0:
            self.speak_dialog('no.appointments.number')
        else:
            if number > len(future_events):
                self.speak(f"You have only {len(future_events)} upcoming events and they are")
                number = len(future_events)
            else:
                self.speak("Your following events are")

            for i in range(number):
                next_event = future_events[i].instance.vevent

                self.helper_speak_event(next_event)

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



def create_skill():
    return CalendarManager()
