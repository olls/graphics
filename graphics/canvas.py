import random
import copy

from . import colors
from . import console
from . import shapes

class Canvas:
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

        self.center = center
        self.border = border

        self.width = size[0]
        self.height = size[1]

        self.background = background

        self.sprites = []

    def __str__( self ):
        """
            Returns the screen as a string, taking
                the Canvas attributes into account.
        """
        # Generate screen
        if isinstance(self.background, str):
            display = [[ str(self.background) for x in range( self.width ) ]
                         for y in range( self.height )]
        else:
            display = copy.deepcopy(self.background)

        # Populate screen with sprites
        for sprite in self.sprites:

            image = sprite.image.image()
            for y, row in enumerate( image ):
                for x, pixel in enumerate( row ):
                    if pixel:
                        try:
                            display[ int( sprite.position[1] + y ) ][ int( sprite.position[0] + x ) ] = \
                                colors.colorStr( sprite.char, sprite.color )
                        except IndexError:
                            pass

        hPad = (
            self.center * (
                int(( console.WIDTH -
                       ( (self.width * 2) -1 ) -
                       ( 4* self.border )
                    )/2 ) * ' '
            )
        )

        # Generate string for screen
        return (
            # Top padding:
            '\n\n' +
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

    def testPixel( self, testPixel ):
        """
            testPixel = ( int x, int y )
        """
        for sprite in self.sprites:
            for y, row in enumerate( sprite.image.image() ):
                for x, pixel in enumerate( row ):
                    if pixel:
                        if ( testPixel[0] == sprite.position[0]+x and
                             testPixel[1] == sprite.position[1]+y ):
                            return True
        return False

    @property
    def height( self ):
        return self._height
    @height.setter
    def height( self, h ):
        if ( h + (self.border *2) ) >= console.HEIGHT:
            raise Exception( 'Canvas too high to fit on console.' )
        self._height = int( h )

    @property
    def width( self ):
        return self._width
    @width.setter
    def width( self, w ):
        if ( ( w + self.border ) *2 ) >= console.WIDTH:
            raise Exception( 'Canvas too wide to fit on console.' )
        self._width = int( w )

    @property
    def border( self ):
        return self._border
    @border.setter
    def border( self, b ):
        self._border = bool( b )

    @property
    def center( self ):
        return self._center
    @center.setter
    def center( self, c ):
        self._center = bool( c )