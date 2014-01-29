

def rotatePosition(pos, size):
    return [pos[1], size[0] - pos[0] - 1]


def rotateImage(image, angle):
    """
        rotates a 2d array to a multiple of 90 deg.
        0 = default
        1 = 90 deg. cw
        2 = 180 deg.
        3 = 90 deg. ccw
    """
    image = [list(row) for row in image]

    for n in range(angle % 4):
        image = list(zip(*image[::-1]))

    return image
