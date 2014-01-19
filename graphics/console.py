import os

class Size:
    def __init__(self):
        self.env = os.environ
        cr = Size.ioctl_GWINSZ( 0 ) or Size.ioctl_GWINSZ( 1 ) or Size.ioctl_GWINSZ( 2 )
        self.method = 1
        if not cr:
            try:
                fd = os.open( os.ctermid(), os.O_RDONLY )
                cr = Size.ioctl_GWINSZ( fd )
                os.close( fd )
            except:
                pass
            self.method = 2
        if not cr:
            cr = ( self.env.get( 'LINES', 25 ), self.env.get( 'COLUMNS', 80 ) )
            self.method = 3

    def getSize(self):
        if self.method == 1:
            cr = Size.ioctl_GWINSZ( 0 ) or Size.ioctl_GWINSZ( 1 ) or Size.ioctl_GWINSZ( 2 )
        elif self.method == 2:
            fd = os.open( os.ctermid(), os.O_RDONLY )
            cr = Size.ioctl_GWINSZ( fd )
            os.close( fd )
        elif self.method == 3:
            cr = ( self.env.get( 'LINES', 25 ), self.env.get( 'COLUMNS', 80 ) )

        return int( cr[1] ), int( cr[0] )

    def ioctl_GWINSZ( fd ):
        try:
            import fcntl, termios, struct, os
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