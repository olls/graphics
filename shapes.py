import math

""" Functions to generate different shapes to be used as sprite images. """

def vector(angle, length):
    """
        angle in degrees
        length in pixels
    """
    xLength = length * math.sin(math.radians(angle))
    yLength = length * math.cos(math.radians(angle))
    image = [[False for x in range(abs(int(xLength))+1)] for y in range(abs(int(yLength))+1)]

    if (angle-45) % 180 < 90:

        if xLength <= 0: # If -ve length --> go backwards
            for xOff in range(0, int(xLength), -1):
                image[int((xLength - xOff) / math.tan(math.radians(angle)))]\
                     [int(xLength - xOff)] = True

        else:
            
            for xOff in range(0, int(xLength), 1):
                image[int((xLength - xOff) / math.tan(math.radians(angle)))]\
                     [int(xLength - xOff)] = True
    
    else:

        if yLength <= 0: # If -ve length --> go backwards
            for yOff in range(0, int(yLength), -1):
                image[int(yLength - yOff)]\
                     [int((yLength - yOff) * math.tan(math.radians(angle)))] = True

        else:
            for yOff in range(0, int(yLength), 1):
                image[int(yLength - yOff)]\
                     [int((yLength - yOff) * math.tan(math.radians(angle)))] = True
    
    return image

def square(size):
    """
        size = (width, height) in pixels
        the char to use
    """
    image = [[False for x in range(size[0])] for y in range(size[1])]

    for xPos in range(0, size[0]):
        for yPos in range(0, size[1]):
            image[yPos][xPos] = True
    return image

def circle(radius):
    """
        radius in pixels
        the char to use
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