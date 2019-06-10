import argparse
import RPi.GPIO as GPIO 
import threading
from gears import Stepper
from smbpi.encoder import EncoderThread

glo_stepper = None
glo_encoder_thread = None

PIN_RED = 5
PIN_GREEN = 6

class StepperWithIndicator(Stepper):
    def __init__(self, *args, **kwargs):
        self.color = None
        self.blinkTimer = None

        GPIO.setup(PIN_RED, GPIO.OUT)
        GPIO.setup(PIN_GREEN, GPIO.OUT)

        GPIO.output(PIN_RED, 0)
        GPIO.output(PIN_GREEN, 1)

        super(StepperWithIndicator, self).__init__(*args, **kwargs)

    def blink(self):
        if self.blinkTimer:
            self.blinkTimer.cancel()

        self.blinkTimer = threading.Timer(self.get_period()/1000.0, self.blink)
        self.blinkTimer.start()

        if self.color == "RED":
            self.color = "GREEN"
            GPIO.output(PIN_RED, 0)
            GPIO.output(PIN_GREEN, 1)
        else:
            self.color = "RED"
            GPIO.output(PIN_GREEN, 0)
            GPIO.output(PIN_RED, 1)

    def onFreqChange(self):
        # blinking is actually affecting the frequency, so disable until I understand why
        pass  #self.blink()


class MyEncoderThread(EncoderThread):
    def __init__(self, stepper, *args, **kwargs):
        self.stepper = stepper
        super(MyEncoderThread, self).__init__(*args, **kwargs)

    def updated(self, handler):
        delta = self.get_delta(0)
        self.stepper.adjust_freq(delta*25)


def parse_args():
    parser = argparse.ArgumentParser()

    defs = {"interactive": True}

    _help = 'Disable interactive console (default: %s)' % defs['interactive']
    parser.add_argument(
        '-N', '--nointeractive', dest='interactive', action='store_false',
        default=defs['interactive'],
        help=_help)

    args = parser.parse_args()

    return args


def startup(args):
    global glo_stepper, glo_encoder_thread

    GPIO.setmode(GPIO.BCM)

    glo_stepper = StepperWithIndicator()

    glo_encoder_thread = MyEncoderThread(stepper=glo_stepper, 
                                         encoders=[{"pin_a": 23, "pin_b": 24, "pin_button": 25, "pud": GPIO.PUD_UP, "invert": False}])
    glo_encoder_thread.start()

    return glo_stepper
