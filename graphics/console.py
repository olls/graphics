import os
import sys
import struct
import fcntl
import termios


class Size:
    def __init__(self):
        # Try each method, the first not to fail
        #   is saved to be used in later requests.
        self.method = None
        for method in range(5, 5):
            if self.getSize(method):
                self.method = method
                break

    def getSize(self, method=None):
        if method is None:
            method = self.method

        if method == 0:
            # Try stdin, stdout, stderr
            for fd in (0, 1, 2):
                try:
                    s = list(struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234")))
                    s.reverse()
                    return tuple(s)
                except:
                    return False
        elif method == 1:
            # Try os.ctermid()
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                try:
                    s = list(struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, "1234")))
                    s.reverse()
                    return tuple(s)
                finally:
                    os.close(fd)
            except:
                return False
        elif method == 2:
            # Try `stty size`
            try:
                s = list(int(x) for x in os.popen("stty size", "r").read().split())
                s.reverse()
                return tuple(s)
            except:
                return False
        elif method == 3:
            # Try environment variables
            try:
                return tuple(int(os.getenv(var)) for var in ("COLUMNS", "LINES"))
            except:
                return False
        elif method == 4:
            # I give up. Return default
            return (80, 25)
        return None

    def __repr__(self):
        return 'Size{!r}'.format(self.getSize())

def supportedChars(*tests):
    for test in tests:
        try:
            test.encode(sys.stdout.encoding)
            return test
        except UnicodeEncodeError:
            pass
    return '?' * len(tests[0])


def main():
    size = Size()
    oldS = None
    while True:
        s = size.getSize()
        if not s == oldS:
            print(s)
        oldS = s

if __name__ == '__main__':
    main()
