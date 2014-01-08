Python Text Based Graphics Module
=================================

This is a console based graphics engine for simple ASCII games or animations.

Usage
=====

`clock.py` and `example.py` are example programs using the module.

Simple usage example:

```
import sys

import graphics
import shapes

# Create the canvas 20x20 pixels (characters).
screen = graphics.Canvas(size=(20, 20))

# Create a circle image, radius 5 pixels.
circleImage = shapes.Circle(5)

# Create a sprite with the circle image
circleSprite = graphics.Sprite(circleImage)

# Add the sprite in green to the canvas at (7, 7).
screen.addSprite(circleSprite, pos=(7, 7), color=graphics.colors.GREEN)

# Output the canvas to the terminal.
print(screen)

# Increase the circles radius by two.
circleSprite.img.incRadius(2)

# Output the canvas to the terminal.
sys.stdout.write(screen)
```

Note: You have to use sys.stdout.write() to output the canvas to get the colors.

Files
=====

`console.py` is a small script to determine the terminal size. Works in my gnome-terminal in Debian, probably wont work in all environments, was not written by me, I think it came off a stack overflow.

`colors.py` has functions for adding the correct escapes to strings to color them, also off stack overflow, also not sure about environment support.

`nbinput.py` an object to get non blocking input in the terminal, this only works in Linux terminals.