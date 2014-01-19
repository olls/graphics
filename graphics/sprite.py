import random
import copy

from . import colors
from . import shapes

class Sprite:
    def __init__( self, image, position=(0, 0), color=None, char=None ):
        """
            image = Image() instance
            position = ( int x, int y )
            color = int range( 0, 8 )
            char = str char
        """

        self.image = copy.deepcopy( image )
        self.position = [ int( position[0] ), int( position[1] ) ]

        self.color = color if color else random.randint( 1, 8 )
        self._char = str(char)[0] if char else chr( 0x25CF )

    def char(self, pos):
        try:
            char = self.image.char(pos)
        except AttributeError:
            char = self._char
        return char

    def move( self, direction=0 ):
        """
            direction = int range( 0, 4 )

            0 = Down
            1 = Left
            2 = Up
            3 = Right
        """
        direction = int(direction)
        self.position = list(self.position)

        if direction == 0:
            self.position[1] += 1
        elif direction == 1:
            self.position[0] -= 1
        elif direction == 2:
            self.position[1] -= 1
        elif direction == 3:
            self.position[0] += 1

    def touching( self, canvas, side=None ):
        """
            Returns True if touching any pixels [on specified side].

            0 = Bottom
            1 = Left
            2 = Top
            3 = Right
        """
        try:
            side = list(side)
        except TypeError:
            if side is None:
                side = list(range(4))
            else:
                side = [side]

        # Find all edges of shape.
        edges = []
        image = self.image.image()
        width = len(image[0])
        height = len(image)
        if 0 in side:
            # Find bottom edges
            for x in range( width ):
                if image[-1][x] is True:
                    y = height
                else:
                    y = height-1
                    while image[y][x] is False:
                        y -= 1
                    y += 1
                edges.append( (x, y) )
        if 1 in side:
            # Find left edges
            for y in range( height ):
                if image[y][0] is True:
                    x = -1
                else:
                    x = 0
                    while image[y][x] is False:
                        x += 1
                    x -= 1
                edges.append( (x, y) )
        if 2 in side:
            # Find top edges
            for x in range( width ):
                if image[0][x] is True:
                    y = -1
                else:
                    y = 0
                    while image[y][x] is False:
                        y += 1
                    y -= 1
                edges.append( (x, y) )
        if 3 in side:
            # Find right edges
            for y in range( height ):
                if image[y][-1] is True:
                    x = width
                else:
                    x = width-1
                    while image[y][x] is False:
                        x -= 1
                    x += 1
                edges.append( (x, y) )

        # Find if any other sprites are in our edge coords.
        for pixel in edges:
            pixel = ( pixel[0] + int( self.position[0] ),
                      pixel[1] + int( self.position[1] ) )
            if canvas.testPixel( pixel ):
                return True
        return False

    def edge( self, canvas ):
        """
            Returns a list of the sides of the sprite
                which are touching the edge of the canvas.

            0 = Bottom
            1 = Left
            2 = Top
            3 = Right
        """
        sides = []
        if int( self.position[0] ) <= 0:
            sides.append( 1 )

        if ( int( self.position[0] ) + self.image.width ) >= canvas.width:
            sides.append( 3 )

        if int( self.position[1] ) <= 0:
            sides.append( 2 )

        if ( int( self.position[1] ) + self.image.height ) >= canvas.height:
            sides.append( 0 )

        return sides