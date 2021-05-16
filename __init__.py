from mycroft import MycroftSkill, intent_file_handler


from datetime import datetime
import sys

import caldav

from caldav.elements import dav
from caldav.objects import Calendar


class CalendarManager(MycroftSkill):
   
    def __init__(self):
        MycroftSkill.__init__(self)
        

    @intent_file_handler('manager.calendar.intent')
    def handle_manager_calendar(self, message):
        self.speak_dialog('manager.calendar')           #{'date':self.next_appointment.DTSTART}, {'title':self.next_appointment.SUMMARY}
        print(GetDataFromNextcloud.whats_my_next_appointment())

def create_skill():
    return CalendarManager()





class GetDataFromNextcloud():


    def __init__(self):
        self.caldav_url = 'https://si-nextcloud.social-robot.info/remote.php/dav'
        self.username = 'ar140@hdm-stuttgart.de'
        self.password = 'Mycroftgruppe5'

        self.client = caldav.DAVClient(url=self.caldav_url, username=self.username, password=self.password)
        self.the_same_calendar = self.client.calendar(url="https://si-nextcloud.social-robot.info/remote.php/dav/calendars/ar140%40hdm-stuttgart.de/personal/")




    #client = caldav.DAVClient(url)


    # check the calendar events and parse results..

    #if calendars:
        ## Some calendar servers will include all calendars you have
        ## access to in this list, and not only the calendars owned by
        ## this principal.
    #   print("your principal has %i calendars:" % len(calendars))
    #  for c in calendars:
    #        print("    Name: %-20s  URL: %s" % (c.name, c.url))
    #else:
    #   print("your principal has no calendars")

    #try:
        ## This will raise a NotFoundError if calendar does not exist
    #   my_new_calendar = my_principal.calendar(name="Test calendar")
    #  assert(my_new_calendar)
        ## calendar did exist, probably it was made on an earlier run
        ## of this script
    #except caldav.error.NotFoundError:
        ## Let's create a calendar
    #   my_new_calendar = my_principal.make_calendar(name="Test calendar")


    
    # def whats_my_next_appointment(calendar: Calendar):
    def whats_my_next_appointment(self):
        all_events = self.the_same_calendar.events()
        return all_events[0].data

    #next_appointment = whats_my_next_appointment(the_same_calendar)
    