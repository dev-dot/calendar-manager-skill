from datetime import datetime
import sys

import caldav

from caldav.elements import dav
from caldav.objects import Calendar

class GetDataFromNextcloud():


    def __init__(self):
        self.caldav_url = 'https://si-nextcloud.social-robot.info/remote.php/dav'
        self.username = 'ar140@hdm-stuttgart.de'
        self.password = 'Mycroftgruppe5'

        self.client = caldav.DAVClient(url=self.caldav_url, username=self.username, password=self.password)
        self.the_same_calendar = self.client.calendar(url="https://si-nextcloud.social-robot.info/remote.php/dav/calendars/ar140%40hdm-stuttgart.de/personal/")




   
    
    # def whats_my_next_appointment(calendar: Calendar):
    def whats_my_next_appointment(self):
        all_events = self.the_same_calendar.events()
        return all_events[0].data

    #next_appointment = whats_my_next_appointment(the_same_calendar)
    