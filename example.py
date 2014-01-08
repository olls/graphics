import time

import graphics
import shapes

def main():
	screen = graphics.Canvas(size=(20, 20))
	
	line = graphics.Sprite(
		shapes.Vector(0, 10),
		(5, 5)
	)
	screen.addSprite(line)

	while True:
		line.img.incAngle(5)
		
		time.sleep(0.1)
		print(screen)

if __name__ == '__main__':
	main()