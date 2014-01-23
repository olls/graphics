import sys
import select
import tty
import termios
import time


class NonBlockingInput(object):
    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def char(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return False


if __name__ == '__main__':
    # Use like this
    with NonBlockingInput() as nbi:
        while True:

            if nbi.char() == ' ':
                print('A')
            else:
                print('B')
            time.sleep(.1)
