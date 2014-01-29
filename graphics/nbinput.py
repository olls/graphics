import sys
import select
import tty
import termios
import time


class NonBlockingInput:
    """
    Gets a single character from standard input.  Does not echo to the
        screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMacCarbon()
            except (AttributeError, ImportError):
                self.impl = _GetchUnix()

    def char(self): return self.impl.char()
    def __enter__(self): return self.impl.enter()
    def __exit__(self, type_, value, traceback):
        return self.impl.exit(type_, value, traceback)

class _GetchUnix:
    def __init__(self):
        # Import termios now or else you'll get the Unix version on the Mac.
        import tty, sys, termios

    def enter(self):
        import sys, tty, termios
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def exit(self, type_, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def char(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return None


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def enter(self):
        import msvcrt
        return self

    def exit(self, type_, value, traceback):
        pass

    def char(self):
        return msvcrt.getch()

class _GetchMacCarbon:
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.  The
    page http://www.mactech.com/macintosh-c/chap02-1.html was
    very helpful in figuring out how to do this.
    """
    def __init__(self):
        import Carbon
        Carbon.Evt # See if teminal has this (in Unix, it doesn't)

    def enter(self):
        import Carbon
        return self

    def exit(self, type_, value, traceback):
        pass

    def char(self):
        if Carbon.Evt.EventAvail(0x0008)[0]==0: # 0x0008 is the keyDownMask
            return ''
        else:
            # The event contains the following info:
            # (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            #
            # The message (msg) contains the ASCII char which is
            # extracted with the 0x000000FF charCodeMask; this
            # number is converted to an ASCII character with chr() and
            # returned.

            (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)



if __name__ == '__main__':
    # Use like this
    with NonBlockingInput() as nbi:
        while True:

            if nbi.char() == ' ':
                print('A')
            else:
                print('B')
            time.sleep(.1)
