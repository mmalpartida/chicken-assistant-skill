from mycroft import MycroftSkill, intent_file_handler


class ChickenAssistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('assistant.chicken.intent')
    def handle_assistant_chicken(self, message):
        self.speak_dialog('assistant.chicken')


def create_skill():
    return ChickenAssistant()

