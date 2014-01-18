Python Text Based Graphics Module
=================================

This is a console based graphics engine for simple ASCII games or animations.

Usage
-----

`clock.py`, `example.py` and `game.py` are example programs using the module.

Simple usage example:

```python
import graphics as g

# Create the canvas 20x20 pixels (characters).
screen = g.Canvas(size = (20, 20))

# Create a circle image, radius 5 pixels.
circleImage = g.shapes.Circle(5)

# Create a green sprite at position (7, 7) with the circle image.
circleSprite = g.Sprite( circleImage,
                         position = (7, 7),
                         color = g.colors.GREEN )

# Add the sprite to the canvas.
screen.sprites.append(circleSprite)

# Output the canvas to the terminal.
print(screen)

# Increase the circles radius by two.
circleSprite.image.radius += 2

# Output the canvas to the terminal.
print(screen)
```

Compatibility
-------------

This module was written and tested on Debian with gnome-terminal. It should work with most Linux terminals, but some things might be off.
- Colours should work if your terminal supports them, otherwise they won't cause any problems.
- The input module is definitely restricted to Linux.
- In the Windows CMD it doesn't centre properly, colours don't work, it was slow and input doesn't work.

`console.py` is a small script to determine the terminal size. Works in my gnome-terminal in Debian, probably wont work in all environment. It came from [Stack Overflow](https://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python).

`colors.py` has functions for adding the correct escapes to strings to color them, from [a blog](http://blog.mathieu-leplatre.info/colored-output-in-console-with-python.html), also not sure about environment support.

`nbinput.py` an object to get non blocking input in the terminal, this only works in Linux terminals. This was from [Stack Overflow](https://stackoverflow.com/questions/2408560/python-nonblocking-console-input) too.
