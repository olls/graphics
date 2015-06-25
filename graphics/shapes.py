""" Functions to generate different shapes to be used as sprite images. """

import math

from . import funcs


class Image:

    def __init__(self):
        self.direction = 0

    def __repr__(self):
        return (self.__class__.__name__ +
                '(' +
                ', '.join(key + '=' + repr(value)
                          for key, value in self.__dict__.items()) +
                ')')

    def image(self):
        """
            Generates the image using self.genImage(),
            then rotates it to self.direction and returns it.
        """
        self._image = self.genImage()
        self._image = funcs.rotateImage(self._image, self.direction)
        return self._image

    def rotate(self, direction):
        """
            Rotate 90 deg. * CW (direction=1), CCW (direction=-1)
        """
        self.direction += direction

    @property
    def height(self):
        return len(self.image())

    @property
    def width(self):
        return len(self.image()[0])


class Vector(Image):

    """ A Straight Line """

    def __init__(self, angle, length):
        """
            angle = float range(0, 360)
            length = float
        """
        super(Vector, self).__init__()

        self.angle = int(angle)
        self.length = int(length)

    def genImage(self):
        x = int(self.length * math.sin(math.radians(self.angle)))
        y = int(self.length * math.cos(math.radians(self.angle)))

        image = [[False for xPos in range(abs(x) + 1)]
                 for yPos in range(abs(y) + 1)]

        yMirror = False
        xMirror = False
        if y < 0:
            yMirror = True
        if x < 0:
            xMirror = True

        y0 = 0
        x0 = 0
        y1 = abs(y)
        x1 = abs(x)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        if y0 < y1:
            sy = 1
        else:
            sy = -1
        if x0 < x1:
            sx = 1
        else:
            sx = -1

        err = dx - dy
        while not (y0 == y1 and x0 == x1):
            image[y0][x0] = True
            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x0 += sx

            if x0 == x1 and y0 == y1:
                image[y0][x0] = True
                break

            if e2 < dx:
                err += dx
                y0 += sy

        if yMirror:
            image.reverse()
        if xMirror:
            for row in image:
                row.reverse()

        return image


class Square(Image):

    """ A Solid Box """

    def __init__(self, size):
        """
            size = (int width, int height)
        """
        super(Square, self).__init__()

        self.size = [int(size[0]), int(size[1])]

    def genImage(self):
        return [[True for x in range(int(self.size[0]))]
                for y in range(int(self.size[1]))]


class Box(Image):

    """ A Hollow Box """

    def __init__(self, size):
        """
            size = (int width, int height)
        """
        super(Box, self).__init__()

        self.size = [int(size[0]), int(size[1])]

    def genImage(self):
        image = []

        width = int(self.size[0])
        height = int(self.size[1])

        image.append([True] * height)

        for yPos in range(1, width - 1):
            image.append([])

            image[yPos].append(True)

            for xPos in range(height - 2):
                image[yPos].append(False)

            image[yPos].append(True)

        image.append([True] * height)

        return image


class Circle(Image):

    """ A Circle """

    def __init__(self, radius, filled=False):
        """
            radius = int
        """
        super(Circle, self).__init__()

        self.radius = int(radius)
        self.filled = filled

    def genImage(self):
        r = int(self.radius)

        image = [[False for x in range((r * 2) + 1)]
                 for y in range((r * 2) + 1)]

        for x in range(r):

            y = int(math.sqrt((r * r) - (x * x)))

            if self.filled:

                for dy in range(-y, y + 1):
                    image[r + dy][r + x] = True
                    image[r + dy][r - x] = True
                    image[r + x][r - dy] = True
                    image[r - x][r - dy] = True

            else:

                image[r + y][r + x] = True
                image[r - y][r + x] = True
                image[r + y][r - x] = True
                image[r - y][r - x] = True

                image[r + x][r + y] = True
                image[r + x][r - y] = True
                image[r - x][r + y] = True
                image[r - x][r - y] = True

        return image


class Text(Image):

    """ A text string """

    def __init__(self, text=''):
        super(Text, self).__init__()
        self.text = text

    def genImage(self):
        if len(self.text) == 0:
            return [[True], ]
        return [[False if char == ' ' else True for char in self.text], ]

    def char(self, pos):
        if len(self.text) == 0:
            return True
        else:
            return self.text[pos[0]]

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)


class CustImage(Image):

    def __init__(self, image=None):
        super(CustImage, self).__init__()
        self.custImage = image

    def genImage(self):
        return self.custImage

    def char(self, pos):
        return self.custImage[pos[1]][pos[0]]


def main():
    import sys

    for row in Vector(int(sys.argv[1]), int(sys.argv[2])).image():
        for pixel in row:
            if pixel:
                print('#', end='')
            else:
                print(' ', end='')
            print(' ', end='')
        print()

if __name__ == '__main__':
    main()
