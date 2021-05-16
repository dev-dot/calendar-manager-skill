from mycroft import MycroftSkill, intent_file_handler
import GetDataFromNextcloud

class CalendarManager(MycroftSkill):
   
    def __init__(self):
        MycroftSkill.__init__(self)
        

    @intent_file_handler('manager.calendar.intent')
    def handle_manager_calendar(self, message):
        self.speak_dialog('manager.calendar')           #{'date':self.next_appointment.DTSTART}, {'title':self.next_appointment.SUMMARY}


def create_skill():
    return CalendarManager()