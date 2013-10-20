import console
class Canvas(object):
    def __init__(self, height=30, width=40, background=' ', color='#'):
        self.height = height
        self.width = width

        self.OFF = background
        self.ON = color

        self.sprites = []

    def __str__(self):
        display = [[self.OFF for x in range(self.width)] 
                   for y in range(self.height)]
        for sprite in self.sprites:
            for y, row in enumerate(sprite.img):
                for x, pixel in enumerate(row):
                    if pixel:
                        try:
                            display[sprite.pos[0]+y][sprite.pos[1]+x] = self.ON
                        except IndexError:
                            pass

        out = (int((console.HEIGHT-self.height)/2)-2)*'\n'
        out += (' ' * int((console.WIDTH-self.width)/2-15)) + '+-' + ('-' * len((display[0])*2)) + '+'
        out += '\n'
        for row in display:
            out += (' ' * int((console.WIDTH-self.width)/2-15)) + '| '
            for pixel in row:
                out += pixel + ' '
            out += '|\n'
        out += (' ' * int((console.WIDTH-self.width)/2-15)) + '+-' + ('-' * len((display[0])*2)) + '+'
        out += (int((console.HEIGHT-self.height)/2)-2)*'\n'
        return out

    def addSprite(self, image):
        self.sprites.append(image)

    def testPixel(self, testPixel):
        for sprite in self.sprites:
            for y, row in enumerate(sprite.img):
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
    def __init__(self, image, pos=(0, 0)):
        self.image = image
        self.position = list(pos)

    def rotate(self, dir_):
        """ 
            Rotate clockwise (dir_1), or anticlockwise (dir_=-1).
        """
        rotImg = [[0 for x in range(len(self.image))] for y in range(len(self.image[0]))]

        if dir_ == 1:
            fImg = list(self.image)
            fImg.reverse()
        else:
            fImg = self.image
        
        for y, row in enumerate(fImg):
            if dir_ == -1:
                row = list(row)
                row.reverse()
            for x, pixel in enumerate(row):
                rotImg[x][y] = pixel

        self.image = rotImg

    def move(self, dir_=0):
        if dir_ == 0:
            self.position[0] -= 1
        elif dir_ == 1:
            self.position[1] += 1
        elif dir_ == 2:
            self.position[0] += 1
        elif dir_ == 3:
            self.position[1] -= 1

    @property
    def img(self):
        return self.image

    @property
    def pos(self):
        return self.position

    @property
    def height(self):
        return len(self.image)

    @property
    def width(self):
        return len(self.image[0])

    def touching(self, canvas, side=None):
        # Find all edges of shape.
        edges = []
        if side == 0 or side == None:
            # Find top edges
            for x in range(len(self.image[0])):
                if self.image[0][x] == 1:
                    y = -1
                else:
                    y = 0
                    while self.image[y][x] == 0:
                        y += 1
                    y -= 1
                edges.append((y, x))
        if side == 1 or side == None:
            # Find right edges
            for y in range(len(self.image)):
                if self.image[y][-1] == 1:
                    x = len(self.image[0])
                else:
                    x = len(self.image[0])-1
                    while self.image[y][x] == 0:
                        x -= 1
                    x += 1
                edges.append((y, x))
        if side == 2 or side == None:
            # Find bottom edges
            for x in range(len(self.image[0])):
                if self.image[-1][x] == 1:
                    y = len(self.image)
                else:
                    y = len(self.image)-1
                    while self.image[y][x] == 0:
                        y -= 1
                    y += 1
                edges.append((y, x))
        if side == 3 or side == None:
            # Find left edges
            for y in range(len(self.image)):
                if self.image[y][0] == 1:
                    x = -1
                else:
                    x = 0
                    while self.image[y][x] == 0:
                        x += 1
                    x -= 1
                edges.append((y, x))

        # Find if anything other sprites are in our edge coords.
        touching = False
        for pixel in edges:
            pixel = (pixel[0]+self.pos[0], pixel[1]+self.pos[1])
            if canvas.testPixel(pixel):
                touching = True
        return touching

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