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
                  size = (40, 30),
                  fullscreen = False,
                  background = ' ',
                  center = True,
                  border = True ):

        self.center = center
        self.border = border

        self.size = console.Size()
        self.fullscreen = bool(fullscreen)
        if self.fullscreen:
            self.width, self.height = self.updateSize()
        else:
            self.width, self.height = size[0], size[1]

        self.background = background

        self.sprites = []


    def __str__( self ):
        """
            Returns the screen as a string, taking
                the Canvas attributes into account.
        """
        # Get new size if fullscreen
        s = self.size.getSize()
        if self.fullscreen:
            self.width, self.height = self.updateSize()

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
                        pixelPos = [ int( sprite.position[1] + y ), int( sprite.position[0] + x ) ]

                        # Test if pixel position is on canvas.
                        visible = True
                        try:
                            display[ pixelPos[0] ][ pixelPos[1] ]
                        except IndexError:
                            visible = False
                            pass

                        if visible:
                            char = colors.colorStr( sprite.char((x, y)), sprite.color )
                            display[ pixelPos[0] ][ pixelPos[1] ] = char

        hPad = (
            self.center * (
                int(( s[0] -
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
                '\n' * int(( s[1] -
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
                    if pixel and testPixel[0] == sprite.position[0]+x and\
                                  testPixel[1] == sprite.position[1]+y:
                            return True
        return False

    def updateSize( self ):
        s = self.size.getSize()
        return int((s[0]/2)-5), int(s[1]-5)

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