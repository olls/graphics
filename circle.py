import graphics as g
import time

screen = g.Canvas( size=(21, 21) )

circle = g.Sprite(
    g.shapes.Circle( 0 ),
    (10, 10)
)
screen.addSprite( circle )

circleDir = True
i = 0

while True:

    if circleDir:
        circle.img.incRadius( 1 )
    else:
        circle.img.incRadius( -1 )

    radius = circle.img.radius
    if radius == 10:
        circleDir = False
    elif radius == 1:
        circleDir = True

    circle.setPos( (10 - radius, 10 - radius) )
    circle.setColor( int( i /4 ) %8 )

    print( screen )
    time.sleep( .02 )

    i += 1