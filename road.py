import random
import time

import graphics as g


class Road(g.shapes.Image):

    def __init__(self, width, height, gap):
        super(Road, self).__init__()

        self.gap = gap
        self.spaceBefore = int((width - gap - 2) / 2)
        self.row = (
            [False] * self.spaceBefore +
            [True] +
            [False] * gap +
            [True] +
            [False] * self.spaceBefore
        )

        self.road = [self.row] + [[False] * width] * (height - 1)
        for y in range(height):
            self.move()

    def genImage(self):
        return self.road

    def move(self):
        width = len(self.row)

        prevSpaceBefore = self.spaceBefore

        if prevSpaceBefore == 0:
            change = random.randint(0, 1)
        elif prevSpaceBefore == width - self.gap - 2:
            change = random.randint(-1, 0)
        else:
            change = random.randint(-1, 1)

        self.spaceBefore = prevSpaceBefore + change
        spaceAfter = width - self.spaceBefore - self.gap - 2

        self.road.append(
            [False] * self.spaceBefore +
            [True] +
            [False] * self.gap +
            [True] +
            [False] * spaceAfter
        )
        self.road = self.road[1:]
        return self.road


def main():
    screen = g.Canvas(fullscreen=True)

    player = g.Sprite(
        g.shapes.Circle(1),
        position=(int(screen.width / 2), 1)
    )
    road = g.Sprite(
        Road(screen.width, screen.height, int(screen.width / 3))
    )
    score = g.Sprite(
        g.shapes.Text('Score: 0')
    )

    screen.sprites.append(player)
    screen.sprites.append(road)
    screen.sprites.append(score)

    lastFrame = time.time()
    with g.NonBlockingInput() as nbi:
        while not player.overlaps(screen, exclude=score):
            ch = nbi.char()
            if ch == ',':
                player.move(g.LEFT)
            if ch == '.':
                player.move(g.RIGHT)

            if time.time() - lastFrame >= .05:

                # Increase Score
                score.image.text = (score.image.text[:7] +
                                    str(int(score.image.text[7:]) + 1))

                road.image.move()

                print(screen, end='')
                lastFrame = time.time()

if __name__ == '__main__':
    main()
