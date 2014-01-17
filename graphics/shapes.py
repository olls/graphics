""" Functions to generate different shapes to be used as sprite images. """

import math

class Image( object ):
    def rotate( self, direction ):
        """
            Rotate 90 deg. * CW (direction=1), CCW (direction=-1)
        """
        self.direction += direction

    def _rotate( self, image, direction ):
        """
            Rotate to a multiple of 90 deg.
            0 = default
            1 = 90 deg. CW
            2 = 180 deg.
            3 = 90 deg. CCW
        """
        image = [ list( row ) for row in image ]

        for n in range( direction % 4 ):
            i = [ [ 0 for x in range(len( image )) ] for y in range(len( image[0] )) ]

            for y, row in enumerate( image ):
                for x, pixel in enumerate( row ):
                    i[x][y] = pixel

            [ i[y].reverse() for y, row in enumerate( i ) ]
            image = i

        return image


    @property
    def height( self ):
        return len( self.image() )

    @property
    def width( self ):
        return len( self.image()[0] )


class Vector(Image):
    """ A Straight Line """
    def __init__( self, angle, length ):
        """
            angle = float range( 0, 360 )
            length = float
        """
        self.angle = int( angle )
        self.length = int( length )
        self.direction = 0

    def image( self ):
        x = int( self.length * math.sin(math.radians( self.angle )) )
        y = int( self.length * math.cos(math.radians( self.angle )) )

        image = [ [ False for xPos in range(abs( x ) +1) ]
                    for yPos in range(abs( y ) +1) ]

        yMirror = False
        xMirror = False
        if y < 0:
            yMirror = True
        if x < 0:
            xMirror = True

        y0 = 0
        x0 = 0
        y1 = abs( y )
        x1 = abs( x )

        dy = abs( y1 - y0 )
        dx = abs( x1 - x0 )

        if y0 < y1:
            sy = 1
        else:
            sy = -1
        if x0 < x1:
            sx = 1
        else:
            sx = -1

        err = dx - dy
        while not ( y0 == y1 and x0 == x1 ):
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

        return self._rotate( image, self.direction )

class Square( Image ):
    """ A Hollow Box """
    def __init__( self, size ):
        """
            size = ( int width, int height )
        """
        self.size = [ int( size[0] ), int( size[1] ) ]
        self.direction = 0

    def image( self ):
        return self._rotate(
            [[ False for x in range(int( self.size[0] )) ]
               for y in range(int( self.size[1] )) ],
            self.direction
        )

class Box( Image ):
    """ A Solid Box """
    def __init__( self, size ):
        """
            size = ( int width, int height )
        """
        self.size = [ int( size[0] ), int( size[1] ) ]
        self.direction = 0

    def image( self ):
        image = []

        width = int( self.size[0] )
        height = int( self.size[1] )

        image.append( [True] * height )

        for yPos in range( 1, width -1 ):
            image.append( [] )

            image[yPos].append( True )

            for xPos in range( height -2 ):
                image[yPos].append( False )

            image[yPos].append( True )

        image.append( [True] * height )

        return self._rotate( image, self.direction )

class Circle( Image ):
    """ A Circle """
    def __init__( self, radius ):
        """
            radius = int
        """
        self.radius = int( radius )
        self.direction = 0

    def image( self ):
        r = int( self.radius )

        image = [[ False for x in range( ( r*2 ) +1 ) ]
                   for y in range( ( r*2 ) +1 ) ]

        for x in range( r ):

            y = int( math.sqrt( (r*r) - (x*x) ) )

            image[ r + y ][ r + x ] = True
            image[ r - y ][ r + x ] = True
            image[ r + y ][ r - x ] = True
            image[ r - y ][ r - x ] = True

            image[ r + x ][ r + y ] = True
            image[ r + x ][ r - y ] = True
            image[ r - x ][ r + y ] = True
            image[ r - x ][ r - y ] = True

        return self._rotate( image, self.direction )

class Pixle( Image ):
    """ A Single Pixel """
    def __init__( self ):
        self.direction = 0

    def image( self ):
        return ((True,),)

def main():
    import sys

    for row in Vector( int( sys.argv[1] ), int( sys.argv[2] ) ).image():
        for pixel in row:
            if pixel:
                print( '#', end='' )
            else:
                print( ' ', end='' )
            print( ' ', end='' )
        print()

if __name__ == '__main__':
    main()