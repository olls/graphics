import time
import random as r
import math as m

import graphics as g

def main():
    size = int( min( g.console.WIDTH /2,
                     g.console.HEIGHT ) -1 )

    center = size * .5

    # Generate background
    background = [[' ' for x in range(size)] for y in range(size)]

    hours = 12
    for n in range(1, hours+1):
        angle = n * ( 2*m.pi / hours )

        x = 0.8 * center * m.sin( angle )
        y = 0.8 * center * m.cos( angle )

        for offset, char in enumerate(list(str(n))):
            background[int( center - y )][int( center + x + offset )] = g.colors.colorStr(char, n%8)


    screen = g.Canvas( size=(size, size), border=False, background=background )

    # Clock Face
    screen.sprites.append(
        g.Sprite(
            g.shapes.Circle( center ),
            color = g.colors.CYAN
        )
    )

    # Hands
    second = g.Sprite(
        g.shapes.Vector( 0, center *0.9 ),
        color = g.colors.RED,
        char = chr( 0x25CB )
    )
    minute = g.Sprite(
        g.shapes.Vector( 0, center *0.75 ),
        color = g.colors.YELLOW
    )
    hour = g.Sprite(
        g.shapes.Vector( 0, center *0.5 ),
        color = g.colors.YELLOW
    )
    screen.sprites.append( second )
    screen.sprites.append( minute )
    screen.sprites.append( hour )

    frames = 0
    start = time.time()
    try:
        while True:
            t = int( time.time() )

            for hand, secPerRev in [ ( second, 60 ),
                                     ( minute, 3600 ),
                                     ( hour, 43200 ) ]:

                # +180 and -angle are to compensate for
                #   flipped upside-down angles.
                angle = (( ( t * (360 / secPerRev) ) +180 ) %360)
                hand.image.angle = -angle

                width, height = hand.image.width, hand.image.height

                if angle > 0 and angle <= 90:
                    hand.position = (center - width, center)

                elif angle > 90 and angle <= 180:
                    hand.position = (center - width, center - height)

                elif angle > 180 and angle <= 270:
                    hand.position = (center, center - height)

                elif angle > 270 and angle <= 360:
                    hand.position = (center, center)

            print( screen, end='' )
            time.sleep( 0.1 )
            frames += 1
    except KeyboardInterrupt:
        print( '\nAvg FPS: '+ str( frames / (time.time() - start) ))

if __name__ == '__main__':
    main()