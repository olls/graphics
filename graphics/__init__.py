import random
import copy

from . import colors
from . import console
from . import nbinput

from . import canvas
from . import sprite
from . import shapes

BOTTOM, DOWN, LEFT, TOP, UP, RIGHT = 0, 0, 1, 2, 2, 3

Canvas = canvas.Canvas
Sprite = sprite.Sprite
NonBlockingInput = nbinput.NonBlockingInput
BlockingInput = nbinput.BlockingInput
