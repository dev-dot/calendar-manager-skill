from mycroft import MycroftSkill, intent_file_handler
import GetDataFromNextcloud as data

class CalendarManager(MycroftSkill):
   
    def __init__(self):
        MycroftSkill.__init__(self)
       ## self.data = get_data()
    

    @intent_file_handler('ask.next.appointment.intent_next-appointment')
    def handle_manager_calendar(self, message):
        next_appointment = data.GetDataFromNextcloud.whats_my_next_appointment()
        self.speak_dialog('manager.calendar', {'date':next_appointment.DTSTART}, {'title':next_appointment.SUMMARY})


def create_skill():
    return CalendarManager()