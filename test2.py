import maestro
import time

servo = maestro.Controller('/dev/ttyAMA0')
servo.runScriptSub(0)
print("sub0")
