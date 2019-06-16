import argparse
import RPi.GPIO as GPIO 
import threading
from stepper import Stepper
from smbpi.encoder import EncoderThread
import pigpio

glo_stepper = None
glo_encoder_thread = None

PIN_RED = 5
PIN_GREEN = 6

class StepperWithIndicator(Stepper):
    def __init__(self, shutdownTimeout=0, *args, **kwargs):
        self.color = None
        self.blinkTimer = None
        self.shutdownTimer = None
        self.shutdownTimeout = shutdownTimeout

        GPIO.setup(PIN_RED, GPIO.OUT)
        GPIO.setup(PIN_GREEN, GPIO.OUT)
        GPIO.output(PIN_RED, 1)
        GPIO.output(PIN_GREEN, 1)

        super(StepperWithIndicator, self).__init__(*args, **kwargs)

    def blink(self):
        if self.blinkTimer:
            self.blinkTimer.cancel()

        self.blinkTimer = threading.Timer(self.get_period()/1000.0, self.blink)
        self.blinkTimer.start()

        if not self._enabled:
            GPIO.output(PIN_RED, 1)
            GPIO.output(PIN_GREEN, 1)
        elif self.color == "RED":
            self.color = "GREEN"
            GPIO.output(PIN_RED, 0)
            GPIO.output(PIN_GREEN, 1)
        else:
            self.color = "RED"
            GPIO.output(PIN_GREEN, 0)
            GPIO.output(PIN_RED, 1)

    def onFreqChange(self):
        # if using crappy software PWM, then blinking will affect the frequency generated
        if self._pigpio:
            self.blink()

    def autoShutdown(self):
        self.enable(False)

    def enable(self, state):
        if state and self.shutdownTimeout > 0:
            if self.shutdownTimer:
                self.shutdownTimer.cancel()
            self.shutdownTimer = threading.Timer(self.shutdownTimeout, self.autoShutdown)
            self.shutdownTimer.start()
        super(StepperWithIndicator, self).enable(state)
        self.blink()


class MyEncoderThread(EncoderThread):
    def __init__(self, stepper, *args, **kwargs):
        self.stepper = stepper
        super(MyEncoderThread, self).__init__(*args, **kwargs)

    def updated(self, handler):
        delta = self.get_delta(0)
        self.stepper.adjust_freq_percent(delta)

        if self.get_button_up_event(0):
            if self.stepper.get_enabled():
                self.stepper.enable(False)
            else:
                self.stepper.enable(True)


def parse_args():
    parser = argparse.ArgumentParser()

    defs = {"interactive": True,
            "on": False,
            "microsteps": 4,
            "shutdown": 120,
            "maxfreq": 1000,
            "freq": 100}

    _help = 'Disable interactive console (default: %s)' % defs['interactive']
    parser.add_argument(
        '-N', '--nointeractive', dest='interactive', action='store_false',
        default=defs['interactive'],
        help=_help)

    _help = 'Set number of microsteps (default: %d)' % defs['microsteps']
    parser.add_argument(
        '-m', '--microsteps', dest='microsteps', action='store', type=int,
        default=defs['microsteps'],
        help=_help)

    _help = 'Set maximum frequency (default: %d)' % defs['maxfreq']
    parser.add_argument(
        '-x', '--maxfreq', dest='maxfreq', action='store', type=int,
        default=defs['maxfreq'],
        help=_help)

    _help = 'Set startup frequency (default: %d)' % defs['freq']
    parser.add_argument(
        '-f', '--freq', dest='freq', action='store', type=int,
        default=defs['freq'],
        help=_help)

    _help = 'Turn on at startup (default: %s)' % defs['on']
    parser.add_argument(
        '-o', '--on', dest='on', action='store_true',
        default=defs['on'],
        help=_help)
        
    _help = 'Shutdown timer in seconds (default: %d)' % defs['shutdown']
    parser.add_argument(
        '-s', '--shutdown', dest='shutdown', action='store', type=int,
        default=defs['shutdown'],
        help=_help)        

    args = parser.parse_args()

    return args


def startup(args):
    global glo_stepper, glo_encoder_thread

    GPIO.setmode(GPIO.BCM)

    pig = pigpio.pi()

    glo_stepper = StepperWithIndicator(pigpio=pig,
                                       shutdownTimeout=args.shutdown,
                                       microsteps=args.microsteps,
                                       freq=args.freq,
                                       maxfreq=args.maxfreq)

    glo_encoder_thread = MyEncoderThread(stepper=glo_stepper,
                                         encoders=[{"pin_a": 23, "pin_b": 24, "pin_button": 25, "pud": GPIO.PUD_UP, "button_pud": GPIO.PUD_DOWN, "invert": False}])
    glo_encoder_thread.start()

    if args.on:
        glo_stepper.enable(True)

    return glo_stepper
