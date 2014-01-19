import time
import random

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

    FPS = 10

    screen = g.Canvas( fullscreen=True )

    car = g.Sprite(
        Car()
    )

    image = [[] for i in range(screen.height)]

    llimit = car.image.height
    ulimit = screen.height
    r = ulimit

    for i in range(screen.width):

        tmp = ulimit+1
        while tmp+r <= llimit or tmp+r >= ulimit:
            tmp = random.randint(-2, 2)
        r += tmp

        for y, row in enumerate(image):
            if y == r:
                image[y].append( '@' )
            elif y > r:
                image[y].append( '~' )
            else:
                image[y].append( False )

    ground = g.Sprite(
        g.shapes.CustImage( image ),
        position = (0, 0)
    )

    screen.sprites.append( ground )
    screen.sprites.append( car )

    t = time.time()
    with g.NonBlockingInput() as nbi:
        while True:

            ch = nbi.char()
            if ch == '.':
                car.move( g.RIGHT )
            if ch == ',':
                car.move( g.LEFT )
            if ch == '/':
                car.image.length += 1
            if ch == '\\':
                car.image.length -= 1

            car.move( 2 )
            while not car.touching( screen, side=0 ):
                car.move( 0 )

            if time.time() >= t+(1/FPS):
                t = time.time()
                print( screen )
            time.sleep( .01 )

if __name__ == '__main__':
    main()