import graphics as g
import time

screen = g.Canvas( size=(21, 21) )

circle = g.Sprite(
    g.shapes.Circle( 0, filled = True ),
    (10, 10)
)
screen.sprites.append( circle )

circleDir = True
i = 0

while True:

    if circleDir:
        circle.image.radius += 1
    else:
        circle.image.radius -= 1

    radius = circle.image.radius
    if radius == 10:
        circleDir = False
    elif radius == 1:
        circleDir = True

    circle.position = (10 - radius, 10 - radius)
    circle.color = int( i /4 ) %8

    print( screen )
    time.sleep( .04 )

    i += 1
