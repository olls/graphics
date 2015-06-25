import random
import copy

from . import colors
from . import console
from . import shapes


class Canvas:

    """
        size = (int width, int height)
        fullscreen = bool
        background = char
        center = bool
        border = bool
        wrap = bool
    """

    def __init__(self,
                 size=(40, 30),
                 fullscreen = False,
                 background = ' ',
                 center = True,
                 border = True,
                 wrap = False):

        self.center = center
        self.border = border
        self.bChars = console.supportedChars('╭─╮│╰╯', '┌─┐│└┘', '+-+|++')
        self.wrap = wrap

        self.size = console.Size()
        self.fullscreen = bool(fullscreen)
        if self.fullscreen:
            self.width, self.height = self.updateSize()
        else:
            self.width, self.height = size[0], size[1]

        self.background = background

        self.sprites = []

    def __repr__(self):
        return ('Canvas(size={!r}, fullscreen={!r}, background={!r}, '
                'center={!r}, border={!r}, wrap={!r})'
                ).format(self.size, self.fullscreen,
                         self.background, self.center,
                         self.border, self.wrap)

    def __str__(self):
        """
            Returns the screen as a string, taking
                the Canvas attributes into account.
        """
        consoleSize = self.size.getSize()
        # Get new size if full-screen
        if self.fullscreen:
            self.width, self.height = self.updateSize()

        # Generate screen
        if isinstance(self.background, str):
            display = [[str(self.background) for x in range(self.width)]
                       for y in range(self.height)]
        else:
            display = copy.deepcopy(self.background)

        # Populate screen with sprites
        for sprite in self.sprites:

            image = sprite.image.image()
            for y, row in enumerate(image):
                for x, pixel in enumerate(row):

                    pixelPos = [int(sprite.position[0] + x),
                                int(sprite.position[1] + y)]

                    # Only display pixel if On and
                    #   within bounds if not wrapping.
                    if pixel and (
                            self.withinBounds(pixelPos) or
                            self.wrap):

                        # Wrap position if wrapping enabled.
                        pixelPos = self.wrapPos(pixelPos)

                        # Test if pixel position is on canvas.
                        visible = True
                        try:
                            display[pixelPos[1]][pixelPos[0]]
                        except IndexError:
                            visible = False
                            pass

                        if visible:
                            char = console.supportedChars(sprite.char((x, y)))
                            char = colors.colorStr(char, sprite.color)
                            display[pixelPos[1]][pixelPos[0]] = char

        hPad = (
            self.center * (
                int((consoleSize[0] -
                     ((self.width * 2) - 1) -
                     (4 * self.border)
                     ) / 2) * ' '
            )
        )

        # Generate string for screen
        return (
            # Top padding:
            '\n\n' +
            ('\n' * self.border) +

            # Top border:
            (self.border * (
                hPad +
                self.bChars[0] +
                (self.bChars[1] * ((self.width * 2) + 1)) +
                self.bChars[2] + '\n'
            )) +

            # First line padding
            hPad +
            (self.border * (self.bChars[3] + ' ')) +
            (
                (
                    # Between each line
                    (self.border * (' ' + self.bChars[3])) +
                    '\n' +
                    hPad +
                    (self.border * (self.bChars[3] + ' '))
                ).join(
                    [' '.join(row) for row in display]
                )
            ) +
            (self.border * (' ' + self.bChars[3])) +

            # Bottom border:
            (self.border * (
                '\n' +
                hPad +
                self.bChars[4] +
                (self.bChars[1] * ((self.width * 2) + 1)) +
                self.bChars[5]
            )) +

            # Bottom padding:
            (self.center * (
                '\n' * int((consoleSize[1] -
                            (self.height + (2 * self.border))
                            ) / 2)
            ))
        )

    def testPixel(self, testPixel, excludedSprites=[]):
        """
            testPixel = (int x, int y, [list excludedSprites])
        """
        try:
            excludedSprites = list(excludedSprites)
        except TypeError:
            excludedSprites = [excludedSprites]

        testSprites = [sprite for sprite in self.sprites
                       if sprite not in excludedSprites]

        for sprite in testSprites:
            for y, row in enumerate(sprite.image.image()):
                for x, pixel in enumerate(row):

                    position = [sprite.position[0] + x,
                                sprite.position[1] + y]

                    position = self.wrapPos(position)
                    testPixel = self.wrapPos(testPixel)

                    if (pixel and testPixel[0] == position[0] and
                            testPixel[1] == position[1]):
                        return True
        return False

    def updateSize(self):
        s = self.size.getSize()
        return int((s[0] / 2) - 5), int(s[1] - 5)

    def withinBounds(self, position):
        return (position[0] >= 0 and
                position[0] <= self.width and
                position[1] >= 0 and
                position[1] <= self.height)

    def wrapPos(self, position):
        if self.wrap:
            position = [position[0] % self.width,
                        position[1] % self.height]
        return position

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, b):
        self._border = bool(b)

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, c):
        self._center = bool(c)
