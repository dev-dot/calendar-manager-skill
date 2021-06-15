import datetime
from pdb import main
import sys
from urllib.parse import parse_qs

import caldav
from dateutil import relativedelta
from caldav.elements import dav
from caldav.objects import Calendar

import calendar as calendarday

class GetDataFromNextcloud():


    def __init__(self):
        self.caldav_url = 'https://si-nextcloud.social-robot.info/remote.php/dav'
        self.username = 'ar140@hdm-stuttgart.de'
        self.password = 'Mycroftgruppe5'

        self.client = caldav.DAVClient(url=self.caldav_url, username=self.username, password=self.password)
        self.the_same_calendar = self.client.calendar(url="https://si-nextcloud.social-robot.info/remote.php/dav/calendars/ar140%40hdm-stuttgart.de/personal/")

   
      #  date = datetime.now()
       # current_weekday = calendarday.weekday(date.year, date.month, date.day)
     #   print(current_weekday) #output 6

        
      #  list(calendarday.day_name)['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

       # print(calendarday.day_name[current_weekday])
        #print(self.parse_weekday("tuesday"))
        #print("Test: ",self.search_date_from_weekday(6))
        
      #  dateformat = datetime.now()
     #   print(dateformat)
    #    my_date = datetime.strptime(dateformat, "%Y-%m-%d")
     #   print("test Time ", type(my_date))


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

    def search_date_from_weekday(self, weekday):
        today = datetime.today()
        next_date = today + relativedelta.relativedelta(weekday= weekday)
        return next_date
        
        print(datetime.now().astimezone())

    

   
    
    # def whats_my_next_appointment(calendar: Calendar):
    def whats_my_next_appointment(self):
        all_events = self.the_same_calendar.events()
       # print(all_events)
       # return print(all_events[0].data)

  #  next_appointment = whats_my_next_appointment(the_same_calendar)
    
GetDataFromNextcloud().whats_my_next_appointment()

x = datetime.date.today()

print(x)



## Save

@intent_file_handler('ask.next.appointment.weekday.intent')
def handle_ask_weekday(self,message):

    weekday = message.data['weekday']

    weekday_as_int = self.parse_weekday(weekday)
    if weekday_as_int != "Invalid day of week" :
        event_date = self.search_date_from_weekday(weekday_as_int)

        if (self.parse_weekday(weekday) == event_date.today().weekday()):
            event_date = event_date + timedelta(days=7)
            self.log.info(self.parse_weekday(weekday))
            self.log.info(event_date.today().weekday())
        else:
            event_date = event_date + timedelta(days=0)
            self.log.info(self.parse_weekday(weekday))
            self.log.info(event_date.today().weekday())

        event_date_string = f"{self.get_ordinal_number(event_date.day)} of {event_date.strftime('%B')}"
        start_search = datetime.combine(event_date,datetime.min.time()).astimezone()
        date_end = date(event_date.year,event_date.month,event_date.day+1)
        end_search = datetime.combine(date_end, datetime.min.time()).astimezone()

        calendar = self.get_calendars()[0]
        events = self.get_all_events(calendar= calendar, start= start_search.astimezone(), end= end_search.astimezone())
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
                self.log.info("Start date: %s", start_search)
                self.log.info("End Date: %s", end_search)
    else: 
        self.speak(f"{weekday} is not a weekday. Please rephrase your question.")

    

