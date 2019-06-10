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
                 pigpio=None):
        self._pin_step = pin_step
        self._pin_dir = pin_dir
        self._pin_enable = pin_enable
        self._microsteps = microsteps
        self._steps_per_rev = steps_per_rev
        self._enabled = False
        self._pigpio = pigpio
        self._maxfreq = 4000

        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self._pin_dir, GPIO.OUT)
        GPIO.setup(self._pin_enable, GPIO.OUT)

        GPIO.output(self._pin_dir, 0)
        GPIO.output(self._pin_enable, 0)  # start in disabled state

        self._freq = freq

        if self._pigpio:
            self._pigpio.hardware_PWM(self._pin_step, self._freq, 500000)
        else:
            GPIO.setup(self._pin_step, GPIO.OUT)   # software PWM :(
            self.pwm = GPIO.PWM(self._pin_step, self._freq)    # software PWM :(
            self.pwm.start(50)

    def onFreqChange(self):
        pass

    def set_freq(self, freq):
        self._freq = freq

        if self._pigpio:
            self._pigpio.hardware_PWM(self._pin_step, self._freq, 500000)
        else:
            self.pwm.ChangeFrequency(self._freq)    # software PWM :(

        self.onFreqChange()

    def adjust_freq(self, amount):
        new_freq = min(max(self._freq + amount, 1), self._maxfreq)
        self.set_freq(new_freq)

    def get_freq(self):
        return self._freq

    def get_rpm(self):
        return float(self._freq) * 60.0 / self._microsteps / self._steps_per_rev

    def get_period(self):
        # return milliseconds per revolution
        return 60000 / self.get_rpm()

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