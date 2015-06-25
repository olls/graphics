import time
import random as r
import math

import graphics as g


def main():

    termSize = g.console.Size()
    screen = g.Canvas(border=False)

    # Clock Face
    circle = g.Sprite(
        g.shapes.Circle(0),
        color=g.colors.CYAN
    )
    textTime = g.Sprite(
        g.shapes.Text()
    )
    screen.sprites.append(circle)
    screen.sprites.append(textTime)

    # Hands
    second = g.Sprite(
        g.shapes.Vector(0, 0),
        color=g.colors.RED,
        char=chr(0x25CB)
    )
    minute = g.Sprite(
        g.shapes.Vector(0, 0),
        color=g.colors.YELLOW
    )
    hour = g.Sprite(
        g.shapes.Vector(0, 0),
        color=g.colors.YELLOW
    )
    screen.sprites.append(second)
    screen.sprites.append(minute)
    screen.sprites.append(hour)

    frames = 0
    start = time.time()
    try:
        while True:

            # Update sizes
            termS = termSize.getSize()
            size = int(min(termS[0] / 2,
                           termS[1]) - 1)
            center = size * .5

            screen.width = size
            screen.height = size
            circle.image.radius = center

            # Generate background
            background = [[' ' for x in range(size)]
                          for y in range(size)]

            hours = 12
            for n in range(1, hours + 1):
                angle = n * (2 * math.pi / hours)

                x = 0.8 * center * math.sin(angle)
                y = 0.8 * center * math.cos(angle)

                for offset, char in enumerate(list(str(n))):
                    bac = [slice(int(center - y)),
                           slice(int(center + x + offset))]
                    background[bac[0]][bac[1]] = g.colors.colorStr(char, n % 8)

            screen.background = background

            # Generate hands
            t = int(time.time())

            h = int((t / 3600) % 12)
            h = 12 if h == 0 else h
            m = int((t / 60) % 60)
            s = int((t / 1) % 60)
            textTime.image.text = '{:2}:{:02}:{:02}'.format(h, m, s)
            textTime.position = (center - (len(textTime.image.text) / 2),
                                 (3 / 4) * size)

            for hand, secPerRev, length in [(second, 60, 0.9),
                                            (minute, 3600, 0.75),
                                            (hour, 43200, 0.5)]:
                hand.image.length = center * length

                # +180 and -angle are to compensate for
                #   flipped upside-down angles.
                angle = (((t * (360 / secPerRev)) + 180) % 360)
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

            print(screen, end='')
            time.sleep(0.1)
            frames += 1
    except KeyboardInterrupt:
        print('\nAvg FPS: ' + str(frames / (time.time() - start)))

if __name__ == '__main__':
    main()
