import random as rand
import graphics as g

def main():
    canvas = g.Canvas( fullscreen = True )

    for circles in range(200):
        circle = g.Sprite(
            g.shapes.Circle( 1, filled = True ),
            position = ( rand.randint(0, canvas.width-1),
                         rand.randint(0, canvas.height-1) )
        )
        canvas.sprites.append( circle )
        if circle.edge( canvas ) or circle.touching( canvas ):
            canvas.sprites.remove( circle )
        while not ( circle.edge( canvas ) or circle.touching( canvas ) ):
            circle.image.radius += 1
        # circle.image.radius -=1

    print(canvas)

if __name__ == '__main__':
    main()