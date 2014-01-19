import time

import graphics as g


class Car( g.shapes.Image ):
    def __init__( self, length = 5 ):
        super(Car, self).__init__()
        self.length = length

    def genImage( self ):
        l = self.length
        return [ [ 0 ]+[ 1 for i in range( 2, l ) ]+[ 0 ],
                 [ 1 for i in range( l ) ],
                 [ 0, 1 ]+[ 0 for i in range( 4, l ) ]+[ 1, 0 ] ]

def main():

    FPS = 30

    screen = g.Canvas( size = (20, 10) )

    ground = g.Sprite(
        g.shapes.Vector( 90, 19 ),
        position = (0, 7)
    )
    car = g.Sprite(
        Car()
    )

    screen.sprites.append( ground )
    screen.sprites.append( car )

    with g.NonBlockingInput() as nbi:
        while True:

            if not car.touching( screen, side=0 ):
                car.move( 0 )

            ch = nbi.char()
            if ch == '.':
                car.move( g.RIGHT )
            if ch == ',':
                car.move( g.LEFT )
            if ch == '/':
                car.image.length += 1
            if ch == '\\':
                car.image.length -= 1


            print( screen )
            time.sleep( 1/FPS )

if __name__ == '__main__':
    main()