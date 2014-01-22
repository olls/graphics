import random as rand
import graphics as g

def main():
    print('Please Wait...')
    canvas = g.Canvas( fullscreen = True )

    for circles in range(200):
        circle = g.Sprite(
            g.shapes.Circle( rand.randint(1, int(min(canvas.width/4, canvas.height/2))), filled = True ),
            position = ( rand.randint(0, canvas.width-1),
                         rand.randint(0, canvas.height-1) )
        )
        canvas.sprites.append( circle )
        if circle.edge( canvas ) or circle.touching( canvas ):
            canvas.sprites.remove( circle )

    print(canvas)

if __name__ == '__main__':
    main()
