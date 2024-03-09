from time import sleep
from PIL import Image
import os
import argparse

BLOCKSET = [
    ' ',
    '░',
    '▒',
    '▓',
    '█',
]

BLOCK_COUNT = len(BLOCKSET)

def get_block(r, g, b) -> str:
    brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
    index = int(brightness * BLOCK_COUNT) % BLOCK_COUNT
    return BLOCKSET[index]

def draw(pixels: list[list[tuple[int, int, int]]]):
    out = ''
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row):
            out += get_block(*pixel)
        out += '\n'
    return out

FILL_PIXEL = (255, 255, 0)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)
UP = (0, -1)
def convert_image(image):
    # We're dealing with pngs
    # Overlay to detect transparency
    image = Image.composite(
        image,
        Image.new('RGB', image.size, FILL_PIXEL),
        image
    )
    width, height = image.size

    assert width > 0
    assert height > 0

    pixels: list[list] = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

    direction = RIGHT
    x_min, x_max = (0, width - 1)
    y_min, y_max = (1, height - 1)
    position = (0, 0)
    for _ in range(width * height):
        x, y, = position
        v_x, v_y = direction

        pixels[y][x] = image.getpixel(position)

        position = (x + v_x, y + v_y)
        new_x, new_y = position

        if direction is RIGHT and new_x == x_max:
            direction = DOWN
            x_max -= 1
        elif direction is DOWN and new_y == y_max:
            direction = LEFT
            y_max -= 1
        elif direction is LEFT and new_x == x_min:
            direction = UP
            x_min += 1
        elif direction is UP and new_y == y_min:
            direction = RIGHT
            y_min += 1

        # if turn:
        #     print(draw(pixels))
        #     sleep(0.001)

    return draw(pixels)
    # out = ''
    # for y, row in enumerate(pixels):
    #     for x, pixel in enumerate(row): 
    #         out += get_block(*pixel)
    #     out += '\n'
    # return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    # parser.add_argument(
    #     'integers', metavar='int', nargs='+', type=int,
    #     help='an integer to be summed')
    parser.add_argument(
        '--file', type=str, 
        help='the file where the sum should be written')
    args = parser.parse_args()
    assert os.path.exists(args.file)


    image = Image.open(args.file)
    result = convert_image(image)
    print(result)
