

from time import gmtime
from datetime import date, datetime, timedelta, tzinfo
from mycroft import MycroftSkill, intent_file_handler, audio
import caldav
from caldav.objects import Calendar
import pytz
from lingua_franca.parse import extract_datetime, normalize, extract_number
from lingua_franca.format import nice_date
from tzlocal import get_localzone
from caldav.lib.error import AuthorizationError

class CalendarManager(MycroftSkill):
    """A Mycroft skill for a nextcloud calendar with 4 intent handler.

    This class includes all important intent and helper function for the nextcloud calendar skill.
    The user can change his calendar, ask what's his next appointment,
    appointments on specific dates and his next e.g five appointments.
    """

    def __init__(self):
        """Inits class TODO
        """

        super().__init__()
        self.current_calendar = None
        self.local_tz = get_localzone()
        # If the PI cant change timezone of the device use this variable
       #self.local_tz = pytz.timezone('Europe/Berlin')



    def initialize(self):
        """A lifecycle method from Mycroft.

        The user data is automatically retrieved online if anything has changed.
        """

        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()


    def on_settings_changed(self):
        """Get all credentials for the nextcloud calendar and change it.

        This method changes the settings.js with the credentials,
        if the user changes the credentials online.
        With correct credentilas we can connect to the calendar.
        We catch the authorization error if the credentials are wrong
        and we are not able to connect to the calendar.
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
        """Connects to a calendar with caldav.

        Args:
            caldav_url: valid caldav url from nextcloud calender.
            username: username from nextcloud.
            password: password from nextcloud.

        Returns:
            Returns a client if the user input was successful and a connection could be established.
        """

        try:
            client = caldav.DAVClient(url=caldav_url, username=username, password=password)

            return client
        except Exception as exception:
            self.log.error(exception)
            self.speak("Wrong credentials for calendar access! Please check your Password and Username and your ical url!")
            return


    def get_calendars(self):
        """Get all calenders from nextcloud client

        Returns:
            Returns a list of all calenders
        """

        calendars = self.client.principal().calendars()
        return calendars


    def get_all_events(self, calendar: Calendar, start: datetime = None, end: datetime = None):
        """Get all events from nextcloud calendar.

        If the start is None the calendar returns all events.
        If the start and endtime are not None, we are getting all events from this time period.

        Args:
            calendar : The nextcloud calendar
            start: Optional; Search starttime for the events.
            If not set we get all events. Defaults to None.
            end: Optional; Search endtime for the events. Defaults to None.

        Returns:
            list: Returns a list with the events from the calendar.
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
        """Gets the event title from event.

        Args:
            event ([type]): [description]

        Returns:
            Returns a string with the summary value or if not existing a string.
            For example:

            SUMMARY:Speech Interaction
        """

        try:
            return event.summary.value
        except:
            return "without a title"


    def get_time_string(self, vevent_date: datetime):
        """Get the time und returns only the the hour and minutes.

        Args:
            vevent_date: A datetime object.

        Returns:
            Returns a string with the hour and minutes for the event as a string.
        """

        try:
            time_string = f"{vevent_date.astimezone(self.local_tz).strftime('%H:%M')}"
            return time_string
        except:
            return None


    def get_ordinal_number(self,i):
        """Changes integer numbers to written numbers.

        Args:
            i: The Numbers for the days of the month.

        Returns:
            Returns a day of the month as written numbers.
            For Example:
            1 as first.
            2 as second.
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



    def helper_speak_event(self, event):
        """Helper method for the Mycroft dialogs.

        This Method checks if the event is an all day event,
        goes over more than a day or only for a period of time.
        For every specific case Mycroft has his dialog to speak.

        Args:
            event: The event object from the nextcloud calendar.
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
        """User can change the current calendar

        The method returns a selection of calendars to the user,
        who can then select them numerically. After the user has
        selected a new calendar, it becomes the new current calendar.
        For Example:
        Choose from one of the following calendars by saying the number
        >> one, Persönlich
        >> two, SpeeceInteraction
        >> three, Arbeit
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
        """Intent handler to tell the user his next appointment.

        Gets executed with the right user input.
        The user gets his next appointment in the calendar.
        If there is no appointments left, the user gets a dialog with a fitting message.
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
            self.speak('Your next event is')
            self.log.info(future_events[0].instance.vevent)
            next_event = future_events[0].instance.vevent
            self.helper_speak_event(next_event)


    @intent_file_handler('ask.next.appointment.specific.intent')
    def handle_ask_specific(self, message):
        """Intent handler to tell the user his appointments on specific days.

        Gets executed with the right user input.
        The user can ask e.g for a specific day, or if he has any appointments in two weeks.


        Args:
            message: A message object, which contains the user inputs.
                     In this case the message contains the specific date.
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
        """Intend handler that the user can ask for the next number/amounts of events.

        Gets executed with the right user input.
        The user can ask a specific number of events.
        For example what's his next five events.
        If there es less events than the user asked, Mycroft will tell the remaining events.

        Args:
            message: A message object, which contains the user inputs.
                     In this case the message contains the asked amounts of events. .
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



    @intent_file_handler('ask.create.event.intent')
    def handle_create_event(self):

        calendar = self.current_calendar
        if calendar is None:
            self.speak('No calendar accessible')
            return
        try:
            event_name = self.get_response('Please tell me the name of the event?')

            event_start = self.get_response('What date and time does the event start?')

            if   'all day' in event_start:

                start = extract_datetime(event_start)[0].strftime("%Y%m%d")
                end = (extract_datetime(event_start)[0] + timedelta(days=1)).strftime("%Y%m%d")
            else:

                event_end =  self.get_response('At what date and time ended the event?')
                end = extract_datetime(event_end)[0].strftime("%Y%m%dT%H%M%S")
                start =extract_datetime(event_start)[0].strftime("%Y%m%dT%H%M%S")

            create_date = datetime.now().strftime("%Y%m%dT%H%M%S")

            new_event = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTAMP:{create_date}
DTSTART:{start}
DTEND:{end}
SUMMARY:{event_name}
END:VEVENT
END:VCALENDAR
"""

            if start<end :

                calendar.add_event(new_event)
                self.speak(f"Succesfully created the event {event_name}")
            else:

                self.speak(f"Your event {event_name} will end in the past. Please create a correct event")

        except TypeError as type_error:

            self.log.error(type_error)
            self.speak("not a valid input. Please rephrase your question.")
        except Exception as exception:

            self.log.error(exception)
            self.speak("Unexpected error! Check Logs!")





    @intent_file_handler('ask.delete.event.intent')
    def delete_events(self,message):
        """Intend handler to delete an event.

        This method allows the user to delete any appointments from his nextcloud calendar.
        The user can optional say a date or will be asked. When there is only one appointment,
        Mycroft will ask directy if he should delete the event.
        When there is more than one appointment, Mycroft will create a list of the events
        and the user can choose with saying the number of the list which appointment Mycroft
        should delete.

        Args:
            message: Optional; Ther User can say the date, on which he want to delete an event.
            If the date is not given, Mycroft will ask the date he should delete an event.
        """

        date = message.data.get('date',None)
        try:

            if date is None:
                date = self.get_response('Please tell me the date of the event')


            start_date = extract_datetime(date)[0]
            end_date = datetime.combine(start_date,start_date.max.time())
            calendar = self.current_calendar
            if calendar is None:
                self.speak('No calendar accessible')
                return
            events = self.get_all_events(calendar= calendar, start= start_date.astimezone(self.local_tz), end= end_date.astimezone(self.local_tz))

            if len(events) == 0:
                self.speak_dialog(f"You have no appointments  {date}")
            elif len(events) == 1:
                next_event = events[0]
                summary = self.get_event_title(next_event.instance.vevent)

                shall_be_deleted = self.ask_yesno(f"Do you want to delete this appointment {summary}?")
                if shall_be_deleted == 'yes':

                    next_event.delete()
                    self.speak_dialog('Successfully deleted')

                elif shall_be_deleted == 'no':
                    self.speak_dialog('Canceled deletion')
                else:
                    self.speak_dialog('I could not understand you. Deletion is canceled')
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
                    self.speak(f"You chose {selection}")
                    shall_be_deleted = self.ask_yesno(f"Are you sure to delete this event? ")
                    if shall_be_deleted == 'yes':

                        selected_event.delete()
                        self.speak_dialog('Successfully deleted')

                    elif shall_be_deleted == 'no':
                        self.speak_dialog('Canceled deletion')
                    else:
                        self.speak_dialog('I could not understand you. Deletion is canceled')

                else:
                    self.speak(f"Cancled selection.")
        except TypeError as type_error:

            self.log.error(type_error)
            self.speak(f"{date} is not a valid input. Please rephrase your question.")
        except Exception as exception:
            self.log.error(exception)
            self.speak("Unexpected error! Check Logs!")




    @intent_file_handler('ask.rename.event.intent')
    def rename_event(self,message):

        date = message.data.get('date',None)
        try:

            if date is None:
                date = self.get_response('Please tell me the date of the event you want to rename')


            start_date = extract_datetime(date)[0]
            end_date = datetime.combine(start_date,start_date.max.time())
            calendar = self.current_calendar
            if calendar is None:
                self.speak('No calendar accessible')
                return
            events = self.get_all_events(calendar= calendar, start= start_date.astimezone(self.local_tz), end= end_date.astimezone(self.local_tz))

            if len(events) == 0:
                self.speak_dialog(f"You have no appointments  {date}")
            elif len(events) == 1:
                next_event = events[0]
                summary = self.get_event_title(next_event.instance.vevent)

                shall_be_deleted = self.ask_yesno(f"Do you want to rename this appointment {summary}?")
                if shall_be_deleted == 'yes':
                    new_name = self.get_response("How do you want to call it?")
                    next_event.instance.vevent.summary.value = new_name
                    next_event.save()
                    self.speak_dialog('Successfully renamed')

                elif shall_be_deleted == 'no':
                    self.speak_dialog('Canceled renaming')
                else:
                    self.speak_dialog('I could not understand you. Deletion is canceled')
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
                    self.speak(f"You chose {selection}")
                    shall_be_deleted = self.ask_yesno(f"Are you sure to delete this event? ")
                    if shall_be_deleted == 'yes':

                        selected_event.delete()
                        self.speak_dialog('Successfully deleted')

                    elif shall_be_deleted == 'no':
                        self.speak_dialog('Canceled deletion')
                    else:
                        self.speak_dialog('I could not understand you. Deletion is canceled')

                else:
                    self.speak(f"Cancled selection.")
        except TypeError as type_error:

            self.log.error(type_error)
            self.speak(f"{date} is not a valid input. Please rephrase your question.")
        except Exception as exception:
            self.log.error(exception)
            self.speak("Unexpected error! Check Logs!")


def create_skill():
    """Create the MyCroft Calender Manager Skill.

    Returns:
        Returns the Calender Manager object.
    """

    return CalendarManager()
