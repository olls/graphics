import time
import random

import graphics as g

def main():
    size = int( min( g.console.WIDTH /2,
                     g.console.HEIGHT ) -1 )

    screen = g.Canvas( size=(size, size), border=False )

    center = size * .5

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
        color = g.colors.WHITE,
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
                hand.image.setAngle(-angle)

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