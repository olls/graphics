import time

import graphics as g

def main():
    screen = g.Canvas( size=(20, 20) )

    line = g.Sprite(
        g.shapes.Vector( 0, 10 ),
        (5, 5)
    )
    screen.addSprite( line )

    with g.NonBlockingInput() as nbi:
        while True:

            if nbi.char() == ' ':
                line.img.incAngle( 5 )
                print( screen )

            time.sleep( .01 )

if __name__ == '__main__':
    main()