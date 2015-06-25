import random
import copy

from . import colors
from . import console
from . import shapes
from . import funcs


class Sprite:

    def __init__(self, image, position=(0, 0), color=None, char=None):
        """
            image = Image() instance
            position = (int x, int y)
            color = int range(0, 8)
            char = str char
        """

        self.image = copy.deepcopy(image)
        self.position = [int(position[0]), int(position[1])]

        self.color = color if color else random.randint(1, 8)
        self._char = str(char)[0] if char else console.supportedChars('●', 'O')

    def __repr__(self):
        return ('Sprite({!r}, position={!r}, color={!r}, char={!r})'
                .format(self.image, self.position, self.color, self._char))

    def char(self, pos):
        try:
            char = self.image.char(pos)
            if char is True or char is False:
                raise AttributeError
        except AttributeError:
            char = self._char
        return char

    def move(self, direction=0):
        """
            direction = int range(0, 4)

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

    def touching(self, canvas, side=None):
        """
            Returns True if touching any pixels [on specified side].

            0 = Bottom
            1 = Left
            2 = Top
            3 = Right
            None = All

            This works by creating a list of the image rotated so all the
                requested sides are facing up, then it finds the top edge for
                each image and rotates the coordinates back to the original
                image.
        """
        try:
            sides = list(side)
        except TypeError:
            if side is None:
                sides = list(range(4))
            else:
                sides = [side]

        # Generate rotated images for each direction.
        images = {}
        image = self.image.image()
        for side in sides:
            images.update({
                (side + 2) % 4:
                    funcs.rotateImage(image, (side + 2) % 4)
            })

        # Go through each image finding top edge,
        #   then rotate coordinates to match original image.
        edges = []
        for side, image in images.items():

            for x in range(len(image[0])):
                y = 0
                # If the first pixel is True, no look any further.
                if not image[0][x]:
                    while not image[y][x]:
                        y += 1
                        if y >= len(image):
                            # Fallen off bottom of image, therefore no edge.
                            y = None
                            break

                # Don't do anything if no pixels in column.
                if not y is None:
                    y -= 1  # To get pixel next to pixel which is on.

                    # Get coordinates the right way around.
                    pos = (x, y)
                    size = [len(image), len(image[0])]
                    for i in range(4 - side):
                        size.reverse()
                        pos = funcs.rotatePosition(pos, size)
                    edges.append(pos)

        # Find if any other sprites are in our edge coordinates.
        for pixel in edges:
            pixel = (int(self.position[0] + pixel[0]),
                     int(self.position[1] + pixel[1]))
            if canvas.testPixel(pixel):
                return True
        return False

    def overlaps(self, canvas, exclude=[]):
        """
            Returns True if sprite is touching any other sprite.
        """
        try:
            exclude = list(exclude)
        except TypeError:
            exclude = [exclude]
        exclude.append(self)

        for selfY, row in enumerate(self.image.image()):
            for selfX, pixel in enumerate(row):
                canvasPixelOn = canvas.testPixel(
                    (selfX + self.position[0], selfY + self.position[1]),
                    excludedSprites=exclude
                )
                if pixel and canvasPixelOn:
                    return True
        return False

    def onEdge(self, canvas):
        """
            Returns a list of the sides of the sprite
                which are touching the edge of the canvas.

            0 = Bottom
            1 = Left
            2 = Top
            3 = Right
        """
        sides = []
        if int(self.position[0]) <= 0:
            sides.append(1)

        if (int(self.position[0]) + self.image.width) >= canvas.width:
            sides.append(3)

        if int(self.position[1]) <= 0:
            sides.append(2)

        if (int(self.position[1]) + self.image.height) >= canvas.height:
            sides.append(0)

        return sides
