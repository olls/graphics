import time
import copy

import graphics as g

screen = g.Canvas(size=(21, 21))

circle = g.Sprite(
    g.shapes.Circle(0, filled=True),
    (10, 10)
)
screen.sprites.append(circle)

i = 0

while True:

    radius = circle.image.radius
    if radius == 0:
        radius = 10
        while screen.sprites:
            screen.sprites.pop()
            if len(screen.sprites) > 0:
                print(screen)
                time.sleep(.04)
    else:
        radius -= 1

    circle = copy.deepcopy(circle)
    circle.image.radius = radius
    circle.position = (10 - radius, 10 - radius)
    circle.color += 1
    circle.color %= 8
    screen.sprites.append(circle)

    print(screen)
    time.sleep(.04)

    i += 1
