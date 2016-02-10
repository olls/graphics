import time
import random

import graphics as g


class Car(g.shapes.Image):

    def __init__(self):
        super(Car, self).__init__()

    def genImage(self):
        return [[0, 1, 0], [0, 0, 0], [0, 1, 0]]


def main():

    FPS = 15
    screen = g.Canvas(size=(36, 20))

    touchMeter = g.Sprite(g.shapes.Text(''), color=g.colors.RED)
    mover = g.Sprite(
        Car(),
        color=g.colors.WHITE
    )

    gridImg = ([[False, True, False, False] * 9] + ([[False] * 36]) * 3) * 5
    grid = g.Sprite(
        g.shapes.CustImage(gridImg),
        color=g.colors.GREEN,
        position=(0, 1)
    )

    screen.sprites.append(touchMeter)
    screen.sprites.append(grid)
    screen.sprites.append(mover)

    frame = 0
    t = time.time()
    with g.NonBlockingInput() as nbi:
        while True:

            ch = nbi.char()
            if ch == '.':
                mover.move(g.RIGHT)
            if ch == ',':
                mover.move(g.LEFT)
            if ch == '/':
                mover.move(g.UP)
            if ch == 'm':
                mover.move(g.DOWN)

            str_ = ''
            if mover.touching(screen, 0):
                str_ += str(0)
            if mover.touching(screen, 1):
                str_ += str(1)
            if mover.touching(screen, 2):
                str_ += str(2)
            if mover.touching(screen, 3):
                str_ += str(3)
            if mover.touching(screen):
                str_ += 'T'

            touchMeter.image.text = str_

            if time.time() >= t + (1 / FPS):
                t = time.time()
                print(screen)

if __name__ == '__main__':
    main()
