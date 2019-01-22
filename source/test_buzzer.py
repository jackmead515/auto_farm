import RPi.GPIO as GPIO   #import the GPIO library
import time               #import the time library

class Buzzer:
    def __init__(self):
        GPIO.setup(4, GPIO.IN)
        GPIO.setup(4, GPIO.OUT)
        self.tones = {
            "start": {
                "pitches": [523,988,1047],
                "duration": [0.2,0.2,0.2]
            },
            "error": {
                "pitches": [262,330,0,262,330,0],
                "duration": [0.5,1,0.5,0.5,1,0.5]
            }
        }

    def activate(self, name, count):
        threading.Thread(target=self.play, args=(name, count)).start()

    def play(self, name, count):
        for i in range(count):
            x=0
            for p in self.tones[name]["pitches"]:
              buzzer.buzz(p, self.tones[name]["duration"][x])
              time.sleep(self.tones[name]["duration"][x]*0.5)
              x+=1

    def buzz(self,pitch,duration):
        if(pitch==0):
         time.sleep(duration)
         return
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)

        for i in range(cycles):
         GPIO.output(4, True)
         time.sleep(delay)
         GPIO.output(4, False)
         time.sleep(delay)

if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    buzzer = Buzzer()

    t = input("Enter Tune: ")
    n = input("Count: ")
    buzzer.play(str(t), int(n))
