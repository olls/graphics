Python Text Based Graphics Module
=================================

This is a console based python3 graphics engine for simple Unicode games or animations.

[`clock.py`](http://github.com/olls/graphics/blob/master/clock.py), [`terrain.py`](http://github.com/olls/graphics/blob/master/terrain.py), [`road.py`](http://github.com/olls/graphics/blob/master/road.py), [`input_example.py`](http://github.com/olls/graphics/blob/master/input_example.py) and [`circle.py`](http://github.com/olls/graphics/blob/master/circle.py) are example programs using the module (Note: `<` and `>` are used instead of arrow keys.), also see [grit96](http://github.com/grit96)'s [Physics Engine](http://github.com/grit96/physics-engine) which uses this module.

![terrain.py](http://olls.github.com/graphics/terrain.png "terrain.py")
![road.py](http://olls.github.com/graphics/road.png "road.py")
![clock.py](http://olls.github.com/graphics/clock.png "clock.py")

Usage
-----

Simple usage example:

```python
import graphics as g

# Create the canvas, 20x20 pixels (characters).
screen = g.Canvas(size = (20, 20))

# Create a circle image, radius 5 pixels.
circleImage = g.shapes.Circle(5)

# Create a green sprite at position (7, 7) with the circle image.
circleSprite = g.Sprite(circleImage,
                        position = (7, 7),
                        color = g.colors.GREEN)

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

This module was written and tested with python3 on Debian with gnome-terminal. It should work with most Linux terminals, but some things might be off.
- Colours should work if your terminal supports them, otherwise they won't cause any problems.
- The input module supports Windows, Mac and Unix. Linux works fine and testing is in progress for Windows.
- In the Windows CMD it doesn't centre properly, colours don't work, it was slow and input doesn't work.

[`console.py`](http://github.com/olls/graphics/blob/master/graphics/console.py) is a small script to determine the terminal size. Works in my gnome-terminal in Debian, probably wont work in all environment. It was modified from [Stack Overflow](http://stackoverflow.com/a/3051350/1841416).

[`colors.py`](http://github.com/olls/graphics/blob/master/graphics/colors.py) has functions for adding the correct escapes to strings to color them, modified from [a blog](http://blog.mathieu-leplatre.info/colored-output-in-console-with-python.html), also not sure about environment support.

[`nbinput.py`](http://github.com/olls/graphics/blob/master/graphics/nbinput.py) an object to get non blocking input in the terminal, this only works in Linux terminals. This was modified from [code.activestate.com](http://code.activestate.com/recipes/134892/#c5).


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/olls/graphics/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
