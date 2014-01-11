import sys

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = list(range(8))

def has_colors(stream):
	if not hasattr(stream, 'isatty'):
		return False
	if not stream.isatty():
		return False
	try:
		import curses
		curses.setupterm()
		return curses.tigetnum('colors') > 2
	except:
		return False

has_colors = has_colors(sys.stdout)

def colorStr(text, color=WHITE):
	if has_colors:
		seq = '\x1b[1;%dm' % (30+color) + text + '\x1b[0m'
		return seq
		sys.stdout.write(seq + '\n')
	else:
		return text
		sys.stdout.write(text + '\n')

if __name__ == '__main__':
	# printout('Hello', RED)
	# printout('hi!', YELLOW)

	sys.stdout.write( '\x1b[1;%dm' % (30+MAGENTA) + 
		'This should be the first part!\x1b[0m\x1b[1;%dm' % (30+GREEN) + 
		'This should be the second part!\x1b[0m\n' )