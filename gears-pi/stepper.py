import RPi.GPIO as GPIO 
import time
import pigpio

DEFAULT_PIN_STEP = 18
DEFAULT_PIN_ENABLE = 27
DEFAULT_PIN_DIR = 17


class Stepper(object):
    def __init__(self, 
                 pin_step=DEFAULT_PIN_STEP, 
                 pin_dir=DEFAULT_PIN_DIR, 
                 pin_enable=DEFAULT_PIN_ENABLE, 
                 freq=100,
                 microsteps=4,
                 steps_per_rev=200,
                 maxfreq=1000,
                 pigpio=None):
        self._pin_step = pin_step
        self._pin_dir = pin_dir
        self._pin_enable = pin_enable
        self._microsteps = microsteps
        self._steps_per_rev = steps_per_rev
        self._enabled = False
        self._pigpio = pigpio
        self._maxfreq = maxfreq

        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self._pin_dir, GPIO.OUT)
        GPIO.setup(self._pin_enable, GPIO.OUT)

        GPIO.output(self._pin_dir, 0)
        GPIO.output(self._pin_enable, 0)  # start in disabled state

        self._freq = freq * self._microsteps

        if self._pigpio:
            self._pigpio.hardware_PWM(self._pin_step, self._freq, 500000)
        else:
            GPIO.setup(self._pin_step, GPIO.OUT)   # software PWM :(
            self.pwm = GPIO.PWM(self._pin_step, self._freq)    # software PWM :(
            self.pwm.start(50)

    def onFreqChange(self):
        pass

    def set_freq(self, freq):
        self._freq = int(freq * self._microsteps)

        if self._pigpio:
            self._pigpio.hardware_PWM(self._pin_step, self._freq, 500000)
        else:
            self.pwm.ChangeFrequency(self._freq)    # software PWM :(

        self.onFreqChange()

    def adjust_freq_percent(self, amount):
        amount = amount * self._maxfreq / 100
        print "XXX", amount, self.get_freq()
        new_freq = min(max(self.get_freq() + amount, 1), self._maxfreq)
        print "YYY", new_freq
        self.set_freq(new_freq)

    def set_freq_percent(self, percent):
        percent = min(max(percent, 1), 100)
        self.set_freq(int(self._maxfreq * percent / 100))

    def get_freq(self):
        return self._freq / self._microsteps

    def get_rpm(self):
        return float(self._freq) * 60.0 / self._microsteps / self._steps_per_rev

    def get_period(self):
        # return milliseconds per revolution
        return 60000 / self.get_rpm()

    def get_maxfreq(self):
        return self._maxfreq

    def enable(self, state):
        if state:
            GPIO.output(self._pin_enable, 1)
        else:
            GPIO.output(self._pin_enable, 0)
        self._enabled = state

    def get_enabled(self):
        return self._enabled

def main():
    stepper = Stepper()
    while 1:
        time.sleep(1000)


if __name__ == "__main__":
    main()