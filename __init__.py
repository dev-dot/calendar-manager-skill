from mycroft import MycroftSkill, intent_file_handler


class CalendarManager(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('manager.calendar.intent')
    def handle_manager_calendar(self, message):
        date_type = message.data.('date')
        if date_type is not None:
            self.speak_dialog('manager.calendar' + date_type )


def create_skill():
    return CalendarManager()

    
    
