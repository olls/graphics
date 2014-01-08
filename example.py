import time

import graphics
import shapes
from nbinput import NonBlockingInput

def main():
    screen = graphics.Canvas(size=(20, 20))
    
    line = graphics.Sprite(
        shapes.Vector(0, 10),
        (5, 5)
    )
    screen.addSprite(line)

    with NonBlockingInput() as nbi:
        while True:

            if nbi.char() == ' ':
                line.img.incAngle(5)
                print(screen)

            time.sleep(.1)

if __name__ == '__main__':
    main()