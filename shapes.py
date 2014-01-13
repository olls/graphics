""" Functions to generate different shapes to be used as sprite images. """

import math

class Image(object):
    def rotate(self, dir_):
        """
            Rotate 90 deg. * CW (dir_=1), CCW (dir_=-1)
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
        image = [list(row) for row in image]

        for n in range(dir_ % 4):
            i = [[0 for x in range(len(image))] for y in range(len(image[0]))]

            for y, row in enumerate(image):
                for x, pixel in enumerate(row):
                    i[x][y] = pixel

            [i[y].reverse() for y, row in enumerate(i)]
            image = i

        return image


    @property
    def height(self):
        return len(self.image())

    @property
    def width(self):
        return len(self.image()[0])


class Vector(Image):
    """ A Straight Line """
    def __init__(self, angle, length):
        self._angle = int(angle)
        self._length = int(length)
        self.direction = 0

    @property
    def angle(self):
        return self._angle

    def setAngle(self, angle):
        """ angle in degrees """
        self._angle = int(angle)

    def incAngle(self, amount):
        """ angle in degrees """
        self._angle += int(amount)

    @property
    def length(self):
        return self._length

    def setLength(self, length):
        """ length in pixels """
        self._length = int(length)

    def incLength(self, amount):
        """ length in pixels """
        self._length += int(amount)

    def image(self):
        x = int(self._length * math.sin(math.radians(self._angle)))
        y = int(self._length * math.cos(math.radians(self._angle)))

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
        """ size = (width, height) in pixels """
        self._size = [int(size[0]), int(size[1])]
        self.direction = 0

    @property
    def size(self):
        return self._size

    def setSize(self, size):
        """ size = (width, height) in pixels """
        self._size = int(size)

    def incSize(self, amount):
        """ amount = (width, height) in pixels """
        self._size = (size[0] + int(amount[0]), 
                      size[1] + int(amount[1]))

    def image(self):
        return self._rotate( [ [False for x in range(self.size[0])]
                               for y in range(self.size[1]) ], 
                            self.direction )

class Box(Image):
    """ A Solid Box """
    def __init__(self, size):
        """ size = (width, height) in pixels """
        self._size = [int(size[0]), int(size[1])]
        self.direction = 0

    @property
    def size(self):
        return self._size

    def setSize(self, size):
        """ size = (width, height) in pixels """
        self._size = int(size)

    def incSize(self, amount):
        """ amount = (width, height) in pixels """
        self._size = (size[0] + int(amount[0]), 
                      size[1] + int(amount[1]))

    def image(self):
        image = []

        image.append([True]*self._size[0])
        for yPos in range(1, self._size[0]-2):
            image.append([])

            image[yPos].append(True)
            for xPos in range(self._size[1]-2):
                image[yPos].append(False)
            image[yPos].append(True)
        image.append([True]*self._size[0])

        return self._rotate(image, self.direction)

class Circle(Image):
    """ A Circle """
    def __init__(self, radius):
        """ radius in pixels """
        self._radius = int(radius)
        self.direction = 0

    @property
    def radius(self):
        return self._radius

    def setRadius(self, radius):
        """ radius in pixels """
        self._radius = int(radius)

    def incRadius(self, amount):
        """ radius in pixels """
        self._radius += int(amount)

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