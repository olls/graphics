import os


class Size:
    def __init__(self):
        self.method = 1
        cr = self.getSize()
        if not cr:
            self.method = 2
            try:
                cr = self.getSize()
            except:
                pass
        if not cr:
            self.method = 3
            self.getSize()

    def getSize(self):
        if self.method == 1:
            cr = Size.ioctl_GWINSZ(0) or \
                 Size.ioctl_GWINSZ(1) or \
                 Size.ioctl_GWINSZ(2)
        elif self.method == 2:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = Size.ioctl_GWINSZ(fd)
            os.close(fd)
        elif self.method == 3:
            cr = (self.env.get('LINES', 25), self.env.get('COLUMNS', 80))

        return int(cr[1]), int(cr[0])

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack(
                'hh',
                fcntl.ioctl(
                    fd,
                    termios.TIOCGWINSZ,
                    '1234'
                )
            )
        except:
            return
        return cr

    def __repr__(self):
        return 'Size{!r}'.format(self.getSize())


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
