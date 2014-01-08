import random

import console
import colors

class Canvas(object):
    def __init__(self, size=(40, 30), background=' ', center=True, border=True):
        self.width = int(size[0])
        self.height = int(size[1])

        self.background = background

        self.center = bool(center)
        self.border = bool(border)

        self.sprites = []

    def __str__(self):
        # Generate screen
        display = [[self.background for x in range(self.width+1)] 
                   for y in range(self.height+1)]

        # Populate screen with sprites
        for sprite in self.sprites:
            
            image = sprite.img.image()
            for y, row in enumerate(image):
                for x, pixel in enumerate(row):
                    if pixel:
                        try:
                            display[sprite.pos[0]+y][sprite.pos[1]+x] = colors.colorStr(sprite.char, sprite.color)
                        except IndexError:
                            pass

        hPad = (
            self.center * (
                ' ' * int(( console.WIDTH - ( (self.width*2)-1 ) - ( 4*self.border ) ) /2)
            )
        )
        # Generate string for screen
        return (
            # Top padding:
            '\n' + 
            
            # Top border:
            (self.border * (
                hPad + 
                '╭' + 
                ( '─' * ( (len(display[0]) *2) +1) ) + 
                '╮\n'
            )) + 

            # First line padding
            hPad + 
            ( self.border * '│ ' ) + 
            (
                (
                    # Between each line
                    ( self.border * ' │' ) + 
                    '\n' + 
                    hPad + 
                    ( self.border * '│ ' )
                ).join(
                    [' '.join(row) for row in display]
                )
            ) + 
            ( self.border * ' │' ) + 

            # Bottom border:
            (self.border * (
                '\n' + 
                hPad + 
                '╰' + 
                ('─' * ( (len(display[0]) *2) +1) ) + 
                '╯'
            )) + 

            # Bottom padding:
            (self.center * (
                '\n' * int( ((console.HEIGHT-self.height) /2) - self.border)
            ))
        )

    def addSprite(self, sprite):
        self.sprites.append(sprite)

    def removeSprite(self, sprite):
        self.sprites.remove(sprite)

    def testPixel(self, testPixel):
        for sprite in self.sprites:
            for y, row in enumerate(sprite.img.image()):
                for x, pixel in enumerate(row):
                    if pixel:
                        if testPixel[0] == sprite.pos[0]+y and testPixel[1] == sprite.pos[1]+x:
                            return True
        return False

    @property
    def getHeight(self):
        return self.height

    @property
    def getWidth(self):
        return self.width

    def overlaps(self, sprite):
        overlap = False
        for testSprite in self.sprites:
            if not sprite == testSprite:

                for testY, testRow in enumerate(testSprite.img):
                    for testX, testPixel in enumerate(testRow):
                
                        if testPixel:
                        
                            for y, row in enumerate(sprite.img):
                                for x, pixel in enumerate(row):
                        
                                    if pixel:
                                        if (sprite.pos[0]+y == testSprite.pos[0]+testY and 
                                            sprite.pos[1]+x == testSprite.pos[1]+testX):
                                            overlap = True
        return overlap

class Sprite(object):
    def __init__(self, image, pos=(0, 0), color=None, char=None):
        self.image = image
        self.position = [int(p) for p in pos]

        self._color = color if color else random.randint(1, 8)
        self._char = char[:1] if char else chr(0x25CF)

    def move(self, dir_=0):
        if dir_ == 0:
            self.position[0] -= 1
        elif dir_ == 1:
            self.position[1] += 1
        elif dir_ == 2:
            self.position[0] += 1
        elif dir_ == 3:
            self.position[1] -= 1

    def setImage(self, image):
        self.image = image

    def setPos(self, pos):
        self.position = [int(p) for p in pos]

    def setColor(self, color):
        self._color = color if color in range(8) else self._color

    def setChar(self, char):
        self._char = char[:1]

    @property
    def img(self):
        return self.image

    @property
    def pos(self):
        return self.position

    @property
    def color(self):
        return self._color

    @property
    def char(self):
        return self._char

    def touching(self, canvas, side=None):
        # Find all edges of shape.
        edges = []
        image = self.img.image()
        if side == 0 or side == None:
            # Find top edges
            for x in range(len(image[0])):
                if image[0][x] == 1:
                    y = -1
                else:
                    y = 0
                    while image[y][x] == 0:
                        y += 1
                    y -= 1
                edges.append((y, x))
        if side == 1 or side == None:
            # Find right edges
            for y in range(len(image)):
                if image[y][-1] == 1:
                    x = len(image[0])
                else:
                    x = len(image[0])-1
                    while image[y][x] == 0:
                        x -= 1
                    x += 1
                edges.append((y, x))
        if side == 2 or side == None:
            # Find bottom edges
            for x in range(len(image[0])):
                if image[-1][x] == 1:
                    y = len(image)
                else:
                    y = len(image)-1
                    while image[y][x] == 0:
                        y -= 1
                    y += 1
                edges.append((y, x))
        if side == 3 or side == None:
            # Find left edges
            for y in range(len(image)):
                if image[y][0] == 1:
                    x = -1
                else:
                    x = 0
                    while image[y][x] == 0:
                        x += 1
                    x -= 1
                edges.append((y, x))

        # Find if anything other sprites are in our edge coords.
        for pixel in edges:
            pixel = (pixel[0]+self.pos[0], pixel[1]+self.pos[1])
            if canvas.testPixel(pixel):
                return True
        return False

    def edge(self, canvas):
        sides = []
        if self.pos[0] <= 0:
            sides.append(0)
        if (self.pos[1] + self.width) >= canvas.getWidth:
            sides.append(1)
        if (self.pos[0] + self.height) >= canvas.getHeight:
            sides.append(2)
        if self.pos[1] <= 0:
            sides.append(3)
        return sides

def main():
    import shapes
    import time

    screen = Canvas(size=(20, 20))

    circle = Sprite(
        shapes.Circle(0),
        (10, 10)
    )
    screen.addSprite(circle)

    circleDir = True

    while True:

        if circleDir:
            circle.img.incRadius(1)
        else:
            circle.img.incRadius(-1)

        radius = circle.img.radius
        if radius == 10:
            circleDir = False
        elif radius == 1:
            circleDir = True

        circle.setPos((10-radius, 10-radius))

        print(screen)
        time.sleep(.02)

if __name__ == '__main__':
    main()