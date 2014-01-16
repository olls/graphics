import random
import copy

from . import colors
from . import console
from . import nbinput
from . import shapes

NonBlockingInput = nbinput.NonBlockingInput

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

        if ( ( size[0] + border ) *2 ) +1 > console.WIDTH:
            raise Exception('Canvas to wide to fit on console.')
        if ( size[1] + border ) +1 > console.HEIGHT:
            raise Exception('Canvas to high to fit on console.')

        if not isinstance(background, str) or not len(background) == 1:
            raise TypeError('Canvas attribute background must be a single character.')

        if not isinstance(center, bool):
            raise TypeError('Canvas attribute center must be a boolean.')
        if not isinstance(border, bool):
            raise TypeError('Canvas attribute border must be a boolean.')

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
                 not isinstance( testPixel, tuple ) ):
            raise TypeError( 'Invalid pixel for Canvas.testPixel(): \'{}\''.format(str( testPixel )) )
        if not len( testPixel ) == 2:
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
        self.image = copy.deepcopy( image )
        self.position = [ int( pos[0] ), int( pos[1] ) ]

        self._color = color if color else random.randint( 1, 8 )
        self._char = char[:1] if char else chr( 0x25CF )


    def setImage( self, image ):
        """
            image = Image() instance
        """
        self.image = image

    def setPos( self, pos ):
        """
            pos = ( int x, int y )
        """
        self.position = [ int( pos[0] ), int( pos[1] ) ]

    def move( self, dir_=0 ):
        """
            dir_ = int range( 0, 4 )

            0 = Down
            1 = Left
            2 = Up
            3 = Right
        """
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
        self.position[0] += int( pos[0] )
        self.position[1] += int( pos[1] )

    def changeX( self, amount ):
        """ amount = int dx """
        self.position[1] += int( amount )
    def changeY( self, amount ):
        """ amount = int dy """
        self.position[0] += int( amount )

    def setColor( self, color ):
        """ color = int range( 0, 8 ) """
        self._color = color if color in range( 8 ) else self._color

    def setChar( self, char ):
        """ char = str char """
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