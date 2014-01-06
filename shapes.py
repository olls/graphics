""" Functions to generate different shapes to be used as sprite images. """

import math


class Image(object):
    def rotate(self, dir_):
        """
            Rotate CW (dir_=1), CCW (dir_=-1)
        """
        self.direction += dir_

    def _rotate(self, image, dir_):
        """ 
            Rotate to a multiple of 90 deg.
            0 = default
            1 = 90 deg. CW
            2 = 180 deg.
            3 = 90 deg. CCW
        """
        rotImg = [[0 for x in range(len(image))] for y in range(len(image[0]))]

        if dir_ == 1:
            fImg = list(image)
            fImg.reverse()
        else:
            fImg = image

        for y, row in enumerate(fImg):
            if dir_ == -1:
                row = list(row)
                row.reverse()
            for x, pixel in enumerate(row):
                rotImg[x][y] = pixel

        return rotImg

    @property
    def height(self):
        return len(self.image())

    @property
    def width(self):
        return len(self.image()[0])


class Vector(Image):
    """ A Straight Line """
    def __init__(self, angle, length):
        self._angle = angle
        self._length = length
        self.direction = 0

    @property
    def angle(self):
        return self._angle

    def setAngle(self, angle):
        """
            angle in degrees
        """
        self._angle = angle

    def incAngle(self, amount):
        """
            angle in degrees
        """
        self._angle += amount

    @property
    def length(self):
        return self._length

    def setLength(self, length):
        """
            length in pixels
        """
        self._length = length

    def incLength(self, amount):
        """
            length in pixels
        """
        self._length += amount

    def image(self):
        x = int(length * math.sin(math.radians(self._angle)))
        y = int(length * math.cos(math.radians(self._angle)))

        image = [[False for xPos in range(abs(x)+1)] 
                 for yPos in range(abs(y)+1)]

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

        dy = abs(y1-y0) 
        dx = abs(x1-x0)

        if y0 < y1:
            sy = 1
        else:
            sy = -1
        if x0 < x1:
            sx = 1
        else:
            sx = -1

        err = dx-dy
        while not (y0 == y1 and x0 == x1):
            image[y0][x0] = True
            e2 = 2*err

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

        return self._rotate(image, self.direction)

class Square(Image):
    """ A Hollow Box """
    def __init__(self, size):
        """
            size = (width, height) in pixels
        """
        self._size = size
        self.direction = 0

    @property
    def size(self):
        return self._size

    def setSize(self, size):
        """
            size = (width, height) in pixels
        """
        self._size = size

    def incSize(self, amount):
        """
            amount = (width, height) in pixels
        """
        self._size = (size[0] + amount[0], 
                      size[1] + amount[1])

    def image(self):
        return self._rotate([[False for x in range(size[0])] for y in range(size[1])], self.direction)

class Box(Image):
    """ A Solid Box """
    def __init__(self, size):
        """
            size = (width, height) in pixels
        """
        self._size = size
        self.direction = 0

    @property
    def size(self):
        return self._size

    def setSize(self, size):
        """
            size = (width, height) in pixels
        """
        self._size = size

    def incSize(self, amount):
        """
            amount = (width, height) in pixels
        """
        self._size = (size[0] + amount[0], 
                      size[1] + amount[1])

    def image(size):
        image = [[False for x in range(size[0])] for y in range(size[1])]
        for xPos in range(0, size[0]):
            image[0][xPos] = True
            image[size[1]][xPos] = True

        for yPos in range(0, size[1]):
            image[yPos][0] = True
            image[yPos][size[1]] = True

        return self._rotate(image, self.direction)

class Circle(Image):
    """ A Circle """
    def __init__(self, radius):
        """
            radius in pixels
        """
        self._radius = radius
        self.direction = 0

    @property
    def radius(self):
        return self._radius

    def setRadius(self, radius):
        """
            radius in pixels
        """
        self._radius = radius

    def incRadius(self, amount):
        """
            radius in pixels
        """
        self._radius += amount

    def image(self):
        image = [[False for x in range(self._radius*2+1)] 
                 for y in range(self._radius*2+1)]

        for x in range(self._radius):
            y = int(math.sqrt(self._radius*self._radius - x*x))
            image[self._radius+y][self._radius+x] = True
            image[self._radius-y][self._radius+x] = True
            image[self._radius+y][self._radius-x] = True
            image[self._radius-y][self._radius-x] = True

            image[self._radius+x][self._radius+y] = True
            image[self._radius+x][self._radius-y] = True
            image[self._radius-x][self._radius+y] = True
            image[self._radius-x][self._radius-y] = True

        return self._rotate(image, self.direction)

class Pixle(Image):
    """ A Single Pixel """
    def __init__(self):
        self.direction = 0
        
    def image(self):
        return ((True,),)

def main():
    import sys

    for row in vector(int(sys.argv[1]), int(sys.argv[2])):
        for pixel in row:
            if pixel:
                print('#', end='')
            else:
                print(' ', end='')
            print(' ', end='')
        print()

if __name__ == '__main__':
    main()