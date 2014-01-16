import random
import copy

from . import colors
from . import console
from . import nbinput
from . import shapes

NonBlockingInput = nbinput.NonBlockingInput

def doubleInt(test):
    return not ( not isinstance( test, list ) or
                 not isinstance( test, tuple ) ) or
           not len( test ) == 2 or
           not isinstance( test[0], int ) or
           not isinstance( test[1], int )

class Canvas(object):
    """
        size = (int width, int height)
        background = char
        center = bool
        border = bool
    """
    def __init__( self,
                  size=(40, 30),
                  background=' ',
                  center=True,
                  border=True ):

        if not doubleInt(size):
            raise TypeError( 'Invalid size attribute for Canvas: \'{}\''.format(str( size )) )
        if ( ( size[0] + border ) *2 ) +1 > console.WIDTH:
            raise Exception( 'Canvas to wide to fit on console.' )
        if ( size[1] + border ) +1 > console.HEIGHT:
            raise Exception( 'Canvas to high to fit on console.' )

        if not isinstance(background, str) or not len(background) == 1:
            raise TypeError( 'Canvas attribute background must be a single character: \'{}\''.format(str( background )) )

        if not isinstance(center, bool):
            raise TypeError( 'Canvas attribute center must be a boolean: \'{}\''.format(str( center )) )
        if not isinstance(border, bool):
            raise TypeError( 'Canvas attribute border must be a boolean: \'{}\''.format(str( border )) )

        self.width = int( size[0] )
        self.height = int( size[1] )

        self.background = background[:1]

        self.center = bool( center )
        self.border = bool( border )

        self.sprites = []

    def __str__( self ):
        """
            Returns the screen as a string, taking
                the Canvas attributes into account.
        """
        # Generate screen
        display = [[ self.background for x in range( self.width ) ]
                     for y in range( self.height )]

        # Populate screen with sprites
        for sprite in self.sprites:

            image = sprite.img.image()
            for y, row in enumerate( image ):
                for x, pixel in enumerate( row ):
                    if pixel:
                        try:
                            display[ sprite.pos[1]+y ][ sprite.pos[0]+x ] = \
                                colors.colorStr( sprite.char, sprite.color )
                        except IndexError:
                            pass

        hPad = (
            self.center * (
                int(( console.WIDTH -
                       ( (self.width * 2) -1 ) -
                       ( 4*self.border )
                    )/2 ) * ' '
            )
        )

        # Generate string for screen
        return (
            # Top padding:
            '\n' +
            ( '\n' * self.border ) +

            # Top border:
            (self.border * (
                hPad +
                '╭' +
                ( '─' * ( (self.width *2) +1) ) +
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
                    [ ' '.join(row) for row in display ]
                )
            ) +
            ( self.border * ' │' ) +

            # Bottom border:
            (self.border * (
                '\n' +
                hPad +
                '╰' +
                ('─' * ( (self.width *2) +1) ) +
                '╯'
            )) +

            # Bottom padding:
            (self.center * (
                '\n' * int(( console.HEIGHT -
                             ( self.height + (2 * self.border) )
                           ) /2 )
            ))
        )

    def addSprite( self, sprite ):
        if not isinstance( sprite, Sprite ):
            raise TypeError( 'Invalid sprite for Canvas.addSprite(): \'{}\''.format(str( sprite )) )
        self.sprites.append( sprite )

    def removeSprite( self, sprite ):
        if not isinstance( sprite, Sprite ):
            raise TypeError( 'Invalid sprite for Canvas.removeSprite(): \'{}\''.format(str( sprite )) )
        try:
            self.sprites.remove( sprite )
        except ValueError:
            raise ValueError( 'Sprite not in canvas: \'{}\''.format(str( sprite )) )

    def testPixel( self, testPixel ):
        """
            testPixel = ( int x, int y )
        """
        if not ( not isinstance( testPixel, list ) or
                 not isinstance( testPixel, tuple ) ) or
           not len( testPixel ) == 2
           not isinstance( testPixel[0], int ) or
           not isinstance( testPixel[1], int ):
            raise TypeError( 'Invalid pixel for Canvas.testPixel(): \'{}\''.format(str( testPixel )) )

        for sprite in self.sprites:
            for y, row in enumerate( sprite.img.image() ):
                for x, pixel in enumerate( row ):
                    if pixel:
                        if ( testPixel[0] == sprite.pos[0]+x and
                             testPixel[1] == sprite.pos[1]+y ):
                            return True
        return False

    @property
    def getHeight( self ):
        return self.height

    @property
    def getWidth( self):
        return self.width

    def overlaps( self, sprite ):
        """
            Returns True if sprite is touching any other sprite.
        """
        if not isinstance( sprite, Sprite ):
            raise TypeError( 'Invalid sprite for Canvas.overlaps(): \'{}\''.format(str( sprite )) )

        overlap = False
        for testSprite in self.sprites:
            if not sprite == testSprite:

                for testY, testRow in enumerate( testSprite.img.image() ):
                    for testX, testPixel in enumerate( testRow ):

                        if testPixel:

                            for y, row in enumerate( sprite.img.image() ):
                                for x, pixel in enumerate( row ):

                                    if pixel:
                                        if ( sprite.pos[0]+x == testSprite.pos[0]+testX and
                                             sprite.pos[1]+y == testSprite.pos[1]+testY ):
                                            overlap = True
        return overlap

class Sprite( object ):
    def __init__( self, image, pos=(0, 0), color=None, char=None ):
        """
            image = Image() instance
            pos = ( int x, int y )
            color = int range( 0, 8 )
            char = str char
        """
        if  not isinstance( image, shapes.Image ):
            raise TypeError( 'Invalid image for Sprite(): \'{}\''.format(str( image )) )

        if not doubleInt( pos ):
            raise TypeError( 'Invalid pos for Sprite(): \'{}\''.format(str( testPixel )) )

        if not color == None:
            if not color in range( 0, 8 ):
                raise TypeError( 'Invalid color for Sprite(), must be in range( 0, 8 ): \'{}\''.format(str( color )) )

        if not char == None:
            if not isinstance( char, str ) or\
               not len( char ) == 1:
                raise TypeError( 'Invalid char for Sprite(): \'{}\''.format(str( char )) )

        self.image = copy.deepcopy( image )
        self.position = [ int( pos[0] ), int( pos[1] ) ]

        self._color = color if color else random.randint( 1, 8 )
        self._char = char[:1] if char else chr( 0x25CF )


    def setImage( self, image ):
        """
            image = Image() instance
        """
        if  not isinstance( image, shapes.Image ):
            raise TypeError( 'Invalid image for Sprite.setImage(): \'{}\''.format(str( image )) )

        self.image = image

    def setPos( self, pos ):
        """
            pos = ( int x, int y )
        """
        if not doubleInt( pos ):
            raise TypeError( 'Invalid pos for Sprite.setPos(): \'{}\''.format(str( pos )) )

        self.position = [ int( pos[0] ), int( pos[1] ) ]

    def move( self, dir_=0 ):
        """
            dir_ = int range( 0, 4 )

            0 = Down
            1 = Left
            2 = Up
            3 = Right
        """
        if not isinstance( dir_, int ) or\
           not dir_ in range(0, 4):
            raise TypeError( 'Invalid direction for Sprite.move(): \'{}\''.format(str( dir_ )) )

        if dir_ == 0:
            self.position[1] += 1
        elif dir_ == 1:
            self.position[0] -= 1
        elif dir_ == 2:
            self.position[1] -= 1
        elif dir_ == 3:
            self.position[0] += 1

    def changePos( self, pos ):
        """
            pos = ( int dx, int dy )
        """
        if not doubleInt( pos ):
            raise TypeError( 'Invalid pos increment for Sprite.changePos(): \'{}\''.format(str( pos )) )

        self.position[0] += int( pos[0] )
        self.position[1] += int( pos[1] )

    def changeX( self, increment ):
        """ increment = int dx """
        if not isinstance( increment, int ):
            raise TypeError( 'Invalid increment for Sprite.changeX(): \'{}\''.format(str( increment )) )

        self.position[1] += int( increment )

    def changeY( self, increment ):
        """ increment = int dy """
        if not isinstance( increment, int ):
            raise TypeError( 'Invalid increment for Sprite.changeY(): \'{}\''.format(str( increment )) )

        self.position[0] += int( amount )

    def setColor( self, color ):
        """ color = int range( 0, 8 ) """
        if not color in range( 0, 8 ):
            raise TypeError( 'Invalid color for Sprite.setColor(), must be in range( 0, 8 ): \'{}\''.format(str( color )) )

        self._color = color

    def setChar( self, char ):
        """ char = str char """
        if not isinstance( char, str ) or\
           not len( char ) == 1:
            raise TypeError( 'Invalid char for Sprite.setChar(): \'{}\''.format(str( char )) )

        self._char = char[:1]

    @property
    def img( self ):
        return self.image

    @property
    def pos( self ):
        return self.position

    @property
    def color( self ):
        return self._color

    @property
    def char( self ):
        return self._char

    def touching( self, canvas, side=None ):
        """
            Returns True if touching any pixels [on specified side].

            0 = Bottom
            1 = Left
            2 = Top
            3 = Right
        """
        if not isinstance( canvas, Canvas ):
            raise TypeError( 'Invalid canvas for Sprite.touching(): \'{}\''.format(str( canvas )) )

        if not side == None:
            if not side in range( 0, 4 ):
                raise TypeError( 'Invalid side number for Sprite.touching(), must be in range( 0, 4 ): \'{}\''.format(str( side )) )

        # Find all edges of shape.
        edges = []
        image = self.img.image()
        if side == 0 or side == None:
            # Find bottom edges
            for x in range( self.img.width):
                if image[-1][x] == True:
                    y = self.img.height
                else:
                    y = self.img.height-1
                    while image[y][x] == False:
                        y -= 1
                    y += 1
                edges.append( (x, y) )
        if side == 1 or side == None:
            # Find left edges
            for y in range( self.img.height ):
                if image[y][0] == True:
                    x = -1
                else:
                    x = 0
                    while image[y][x] == False:
                        x += 1
                    x -= 1
                edges.append( (x, y) )
        if side == 2 or side == None:
            # Find top edges
            for x in range( self.img.width ):
                if image[0][x] == True:
                    y = -1
                else:
                    y = 0
                    while image[y][x] == False:
                        y += 1
                    y -= 1
                edges.append( (x, y) )
        if side == 3 or side == None:
            # Find right edges
            for y in range( self.img.height ):
                if image[y][-1] == True:
                    x = self.img.width
                else:
                    x = self.img.width-1
                    while image[y][x] == False:
                        x -= 1
                    x += 1
                edges.append( (x, y) )

        # Find if any other sprites are in our edge coords.
        for pixel in edges:
            pixel = ( pixel[0] + self.pos[0],
                      pixel[1] + self.pos[1] )
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
        if not isinstance( canvas, Canvas ):
            raise TypeError( 'Invalid canvas for Sprite.edge(): \'{}\''.format(str( canvas )) )

        sides = []
        if self.pos[0] <= 0:
            sides.append( 1 )

        if ( self.pos[0] + self.img.width ) >= canvas.getWidth:
            sides.append( 3 )

        if self.pos[1] <= 0:
            sides.append( 2 )

        if ( self.pos[1] + self.img.height ) >= canvas.getHeight:
            sides.append( 0 )

        return sides