import time
import random

import graphics
import shapes

def main():
    size = int(min( graphics.console.WIDTH/2,
                    graphics.console.HEIGHT )-1)

    screen = graphics.Canvas(size=(size, size), border=False)

    center = size * .5

    # Clock Face
    screen.addSprite(
        graphics.Sprite(
            shapes.Circle(center),
            color = graphics.colors.CYAN
        )
    )

    # Hands
    second = graphics.Sprite(
        shapes.Vector(0, center*0.9),
        color = graphics.colors.WHITE,
        char = '*'
    )
    minute = graphics.Sprite(
        shapes.Vector(0, center*0.75),
        color = graphics.colors.YELLOW
    )
    hour = graphics.Sprite(
        shapes.Vector(0, center*0.5),
        color = graphics.colors.YELLOW
    )
    screen.addSprite(second)
    screen.addSprite(minute)
    screen.addSprite(hour)

    frames = 0
    start = time.time()
    try:
        while True:
            t = int(time.time())

            for hand, secPerRev in [(second, 60), (minute, 3600), (hour, 43200)]:

                angle = ((t * (360 / secPerRev)) % 360)+90
                hand.img.setAngle(angle)

                width, height = hand.img.width, hand.img.height

                if angle > 90 and angle <= 180:
                    hand.setPos((center-height, center))
                elif angle > 180 and angle <= 270:
                    hand.setPos((center, center))
                elif angle > 270 and angle <= 360:
                    hand.setPos((center, center-width))
                elif angle > 360 and angle <= 450:
                    hand.setPos((center-height, center-width))

            print(screen, end='')
            time.sleep(0.1)
            frames += 1
    except KeyboardInterrupt:
        print('\nAvg FPS: '+ str( frames / (time.time()-start) ))

if __name__ == '__main__':
    main()