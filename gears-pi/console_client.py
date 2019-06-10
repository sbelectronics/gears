import select
import sys
import termios
import time
import tty

from gears_manager import parse_args, startup


def getchar():
    fd = sys.stdin.fileno()
    old_tcattr = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_tcattr)
    return ch


def main():
    args = parse_args()
    stepper = startup(args)
    last_freq = -1

    if args.interactive:
        print "+ - 10 steps/s faster"
        print "- - 10 steps/s slower"
        print "* - 100 steps/s faster"
        print "/ - 100 steps/s slower"
        print "x - exit"

        print ""

        stdin_fd = sys.stdin.fileno()
        new_term = termios.tcgetattr(stdin_fd)
        old_term = termios.tcgetattr(stdin_fd)
        new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(stdin_fd, termios.TCSAFLUSH, new_term)

        try:
            while True:
                dr,dw,de = select.select([sys.stdin], [], [], 0.1)
                if dr != []:
                    ch = sys.stdin.read(1)

                    if (ch == "+"):
                        stepper.adjust_freq(10)
                    elif (ch == "-"):
                        stepper.adjust_freq(-10)
                    elif (ch == "*"):
                        stepper.adjust_freq(100)
                    elif (ch == "/"):
                        stepper.adjust_freq(-100)
                    elif (ch == "x"):
                        break

                if stepper.get_freq() != last_freq:
                    print "Current:", stepper.get_freq()
                    last_freq = stepper.get_freq()
        finally:
            termios.tcsetattr(stdin_fd, termios.TCSAFLUSH, old_term)

    else:
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main()