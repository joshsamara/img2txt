from typing import reveal_type
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

def get_block(r, g, b, *_, **__) -> str:
    brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
    index = int(brightness * BLOCK_COUNT) % BLOCK_COUNT
    return BLOCKSET[index]


def convert_image(image):
    image.convert('L')
    width, height = image.size



    # TODO: Fix background parsing
    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(
                image.getpixel((x,y))
            )
        pixels.append(row)

    out = ''
    for y, row in enumerate(pixels):
        for x, pixel in enumerate(row): 
            out += get_block(*pixel)
        out += '\n'
    return out

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
    print(convert_image(
        Image.open(args.file)
    ))
