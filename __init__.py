from . import maestro
import random

import time
from os.path import dirname, join
from mycroft import MycroftSkill, intent_handler
from mycroft.skills.audioservice import AudioService
from mycroft.audio import wait_while_speaking


class ChickenAssistant(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.process = None
        self.play_list = {
            0: join(dirname(__file__), "chicken_response_01.mp3"),
            1: join(dirname(__file__), "chicken_response_02.mp3")
        }

    def initialize(self):
        self.audio_service = AudioService(self.bus)
        #self.add_event("mycroft.sing", self.sing, False)

    def sing(self, message):
        self.audioservice.play(self.play_list[0])

    @intent_handler('assistant.chicken.intent')
    def handle_assistant_chicken(self, message):
        path = random.choice(self.play_list)
        try:
            #self.speak_dialog('assistant.chicken')
            #wait_while_speaking()
            self.audio_service.play(path)
            servo = maestro.Controller('/dev/ttyAMA0')
            servo.runScriptSub(0)
            time.sleep(2)
            servo.runScriptSub(1)
            servo.close
           


        except Exception as e:
            self.log.error("Error: {0}".format(e))

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
          


def create_skill():
    return ChickenAssistant()

