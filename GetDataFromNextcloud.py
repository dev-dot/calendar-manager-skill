from datetime import datetime
import sys

import caldav

from caldav.elements import dav
from caldav.objects import Calendar

class GetDataFromNextcloud():


    caldav_url = 'https://si-nextcloud.social-robot.info/remote.php/dav'
    username = 'ar140@hdm-stuttgart.de'
    password = 'Mycroftgruppe5'

    client = caldav.DAVClient(url=caldav_url, username=username, password=password)

    #client = caldav.DAVClient(url)
    my_principal = client.principal()
    # get all available calendars (for this user)
    calendars = my_principal.calendars()
    print(calendars)


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


    the_same_calendar = client.calendar(url="https://si-nextcloud.social-robot.info/remote.php/dav/calendars/ar140%40hdm-stuttgart.de/personal/")

    
    # def whats_my_next_appointment(calendar: Calendar):
    def whats_my_next_appointment(calendar:the_same_calendar):
        all_events = calendar.events()

        return all_events[0].data

    #next_appointment = whats_my_next_appointment(the_same_calendar)
    