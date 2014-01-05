import math

""" Functions to generate different shapes to be used as sprite images. """

def vector_p(y, x):
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

    return image

def vector(angle, length):
    xLength = int(length * math.sin(math.radians(angle)))
    yLength = int(length * math.cos(math.radians(angle)))

    return vector_p(yLength, xLength)

def square(size):
    """
        size = (width, height) in pixels
    """
    return [[False for x in range(size[0])] for y in range(size[1])]

def box(size):
    """
        size = (width, height) in pixels
    """
    image = [[False for x in range(size[0])] for y in range(size[1])]
    for xPos in range(0, size[0]):
        image[0][xPos] = True
        image[size[1]][xPos] = True

    for yPos in range(0, size[1]):
        image[yPos][0] = True
        image[yPos][size[1]] = True

    return image

def circle(radius):
    """
        radius in pixels
    """
    image = [[False for x in range(radius*2+1)] 
             for y in range(radius*2+1)]

    for x in range(radius):
        y = int(math.sqrt(radius*radius - x*x))
        image[radius+y][radius+x] = True
        image[radius-y][radius+x] = True
        image[radius+y][radius-x] = True
        image[radius-y][radius-x] = True

        image[radius+x][radius+y] = True
        image[radius+x][radius-y] = True
        image[radius-x][radius+y] = True
        image[radius-x][radius-y] = True
    return image

def pixel():
    return ((True,),)

def main():
    import sys

    for row in vector(int(sys.argv[1]), int(sys.argv[2])):
        for pixle in row:
            if pixle:
                print('#', end='')
            else:
                print(' ', end='')
            print(' ', end='')
        print()

if __name__ == '__main__':
    main()