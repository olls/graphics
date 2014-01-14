import time

import graphics
import shapes
from nbinput import NonBlockingInput


class Car(shapes.Image):
    def __init__(self, length=5):
        self.length = length

    def image(self):
        l = self.length
        return [[0] + [ 1 for i in range(2, l) ] + [0], 
                [ 1 for i in range(l) ], 
                [ 0, 1 ] + [ 0 for i in range(4, l) ] + [ 1, 0 ]]

def main():

    FPS = 30

    screen = graphics.Canvas( size=(20, 10) )

    ground = graphics.Sprite(
        shapes.Vector( 90, 19 ),
        pos=(0, 7)
    )
    car = graphics.Sprite(
        Car()
    )

    screen.addSprite(ground)
    screen.addSprite(car)

    with NonBlockingInput() as nbi:
        while True:

            if not car.touching( screen, side=0 ):
                car.move( 0 )

            ch = nbi.char()
            if ch == '.':
                car.move( 3 )
            if ch == ',':
                car.move( 1 )
            if ch == '/':
                car.img.length += 1
            if ch == '\\':
                car.img.length -= 1
                

            print( screen )
            time.sleep( 1/FPS )

if __name__ == '__main__':
    main()