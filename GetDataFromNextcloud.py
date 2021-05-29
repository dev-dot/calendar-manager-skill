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
       # print(current_weekday) #output 6

        
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
        
       # print(datetime.now().astimezone())

    

   
    
    # def whats_my_next_appointment(calendar: Calendar):
    def whats_my_next_appointment(self):
        all_events = self.the_same_calendar.events()
       # print(all_events)
       # return print(all_events[0].data)

  #  next_appointment = whats_my_next_appointment(the_same_calendar)
    
GetDataFromNextcloud().whats_my_next_appointment()

x = datetime.date.today()

print(x)