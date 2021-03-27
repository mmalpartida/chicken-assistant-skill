from . import maestro_uart
import random


from os.path import dirname, join
from mycroft import MycroftSkill, intent_handler
from mycroft.skills.audioservice import AudioService
from mycroft.audio import wait_while_speaking

min_pos = 0 #992*4
max_pos = 0 #2000*4
mu = maestro_uart.MaestroUART('/dev/ttyS0', 9600)
channel = 0
error = mu.get_error()
if error:
	print(error)
accel = 5
mu.set_acceleration(channel, accel)
speed = 32
mu.set_speed(channel, speed)
position = mu.get_position(channel)
print('Position is: %d quarter-microseconds' % position)

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
            if position < min_pos+((max_pos - min_pos)/2): # if less than halfway
                target = max_pos
            else:
                target = min_pos
            print('Moving to: %d quarter-microseconds' % target)
            mu.set_target(channel, target)
            mu.close()


        except Exception as e:
            self.log.error("Error: {0}".format(e))

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
          


def create_skill():
    return ChickenAssistant()

