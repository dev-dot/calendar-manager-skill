
from mycroft import MycroftSkill, intent_file_handler


from datetime import datetime
import caldav
from caldav.objects import Calendar

class CalendarManager(MycroftSkill):
   
    def __init__(self):
        MycroftSkill.__init__(self)
        self.caldav_url = 'https://si-nextcloud.social-robot.info/remote.php/dav'
        self.username = 'ar140@hdm-stuttgart.de'
        self.password = 'Mycroftgruppe5'
        self.client = caldav.DAVClient(url=self.caldav_url, username=self.username, password=self.password)
        self.the_same_calendar = self.client.calendar(url="https://si-nextcloud.social-robot.info/remote.php/dav/calendars/ar140%40hdm-stuttgart.de/personal/")

    def get_calendars(self):
        principal = self.client.principal()
        calendars = principal.calendars()

        return calendars

    def whats_my_next_appointment(self, calendar: Calendar):
        all_events = calendar
        return all_events[0].data



    @intent_file_handler('ask.next.appointment.intent')
    def handle_manager_calendar(self, message):
        next_appointment = self.whats_my_next_appointment(self.the_same_calendar)
        print(self.get_calendars()[0])
        self.speak_dialog('next.appointment', {'title':next_appointment["SUMMARY"]})           #{'date':self.next_appointment.DTSTART}, {'title':self.next_appointment.SUMMARY

def create_skill():
    return CalendarManager()