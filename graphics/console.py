import os
import sys
import struct


class Size:

    def __init__(self):
        # Try each method, the first not to fail
        #   is saved to be used in later requests.
        self.method = None
        for method in range(5):
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
                    import termios
                    import fcntl
                    s = list(struct.unpack("hh",
                                           fcntl.ioctl(
                                               fd, termios.TIOCGWINSZ, "1234")
                                           ))
                    s.reverse()
                    return tuple(s)
                except:
                    return False
        elif method == 1:
            # Try os.ctermid()
            try:
                import termios
                import fcntl
                fd = os.open(os.ctermid(), os.O_RDONLY)
                try:
                    s = list(struct.unpack("hh",
                                           fcntl.ioctl(
                                               fd, termios.TIOCGWINSZ, "1234")
                                           ))
                    s.reverse()
                    return tuple(s)
                finally:
                    os.close(fd)
            except:
                return False
        elif method == 2:
            # Try `stty size`
            try:
                size = os.popen("stty size", "r").read().split()
                s = list(int(x) for x in size)
                s.reverse()
                return tuple(s)
            except:
                return False
        elif method == 3:
            # Try environment variables
            try:
                return tuple(
                    int(os.getenv(var)) for var in ("COLUMNS", "LINES")
                )
            except:
                return False
        elif method == 4:
            # I give up. Return default
            return (80, 25)
        return None

    def __repr__(self):
        return 'Size{!r}'.format(self.getSize())


def supportedChars(*tests):
    """
        Takes any number of strings, and returns the first one
            the terminal encoding supports. If none are supported
            it returns '?' the length of the first string.
    """
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
