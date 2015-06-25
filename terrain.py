import time
import random

import graphics as g


class Car(g.shapes.Image):

    def __init__(self, length=5):
        super(Car, self).__init__()
        self.length = length

    def genImage(self):
        l = self.length
        return [[0] + [1 for i in range(2, l)] + [0],
                [1 for i in range(l)],
                [0, 1] + [0 for i in range(4, l)] + [1, 0]]


def genGround(width, height, llimit, ulimit):
    image = [[] for i in range(height)]

    groundPos = int((ulimit + llimit) / 3) * 2

    for i in range(width):

        change = ulimit + 1  # Be sure the 1st iteration of the while will run.
        while change + groundPos <= llimit or change + groundPos >= ulimit:
            change = random.randint(-2, 2)

        yDiff = []
        if change > 0:
            yDiff = list(range(groundPos + 1, groundPos + change))
        elif change < 0:
            yDiff = list(range(groundPos + change, groundPos))

        groundPos += change

        for y, row in enumerate(image):
            if y == groundPos:
                image[y].append(chr(0x25EF))
            elif y in yDiff:
                if change < 0:
                    try:
                        image[y][-1] = chr(0x25FF)
                    except IndexError:
                        pass
                    image[y].append(' ')
                else:
                    image[y].append(chr(0x25FA))
            else:
                image[y].append(False)

    return image


def main():

    FPS = 15
    screen = g.Canvas(fullscreen=True, size=(36, 20), wrap=True)

    frameCount = g.Sprite(g.shapes.Text(''), color=g.colors.RED)
    car = g.Sprite(
        Car(),
        color=g.colors.WHITE
    )

    llimit = screen.height
    ulimit = car.image.height
    grndTerrain = genGround(screen.width,
                            screen.height,
                            car.image.height,
                            screen.height)

    ground = g.Sprite(
        g.shapes.CustImage(grndTerrain),
        color=g.colors.GREEN
    )

    screen.sprites.append(frameCount)
    screen.sprites.append(ground)
    screen.sprites.append(car)

    frame = 0
    frame1 = 0
    t = time.time()
    with g.NonBlockingInput() as nbi:
        while True:
            frame += 1
            frameCount.image.text = str(frame) + ':' + str(frame1)

            ch = nbi.char()
            if ch == '.':
                car.move(g.RIGHT)
            if ch == ',':
                car.move(g.LEFT)
            if ch == '/':
                car.image.length += 1
            if ch == '\\':
                car.image.length -= 1

            car.move(g.UP)
            while not car.touching(screen, side=0):
                car.move(g.DOWN)
            while car.touching(screen, side=0):
                car.move(g.UP)
            car.move(g.DOWN)

            if time.time() >= t + (1 / FPS):
                frame1 += 1
                t = time.time()
                print(screen)

if __name__ == '__main__':
    main()
