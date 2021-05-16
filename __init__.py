from mycroft import MycroftSkill, intent_file_handler
import GetDataFromNextcloud as data

class CalendarManager(MycroftSkill):
   
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('manager.calendar.intent')
    def handle_manager_calendar(self, message):
        self.speak_dialog('manager.calendar')
        print(data.GetDataFromNextcloud.whats_my_next_appointment())


def create_skill():
    return CalendarManager()