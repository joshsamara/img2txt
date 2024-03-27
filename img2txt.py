from PIL import Image
import os
import argparse

BG = '  '
BLOCKSET = [
    '  ',
    '░░',
    '▒▒',
    '▓▓',
    '██',
]

BLOCK_COUNT = len(BLOCKSET)

# Entirely banking on this not conflicting
FILL_COLOR = (254, 255, 253)

def get_block(
    pixel: tuple[int, int, int] | None,
    debug
) -> str:
    if pixel is None:
        return BG

    r, g, b = pixel
    brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
    if debug:
        block = str(f"{int(brightness * 100):2}|")
    else:
        index = int(brightness * BLOCK_COUNT) % BLOCK_COUNT
        block= BLOCKSET[index]

    return block

def serialize(
    pixels: list[list[tuple[int, int, int] | None]],
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    debug: bool,
):
    out = ''
    for y, row in enumerate(pixels):
        y_trim = y < y_min or y > y_max
        draw_row = False
        for x, pixel in enumerate(row):
            trim = y_trim or x < x_min or x > x_max

            if not trim:
                block = get_block(pixel, debug)
                out += block
                draw_row = True

        if draw_row:
            out += '\n'
    return out


def convert_image(filepath, debug: bool = False):
    image = Image.open(filepath).convert('RGBA')
    # We're dealing with pngs
    # Overlay to detect transparency
    image = Image.composite(
        image,
        Image.new('RGB', image.size, FILL_COLOR),
        image
    )
    width, height = image.size

    assert width > 0
    assert height > 0

    # Real pixel boundaries
    x_real_min = width
    y_real_min = height
    x_real_max = 0
    y_real_max = 0

    pixels = [[] for _ in range(height)]
    seen = set()
    for y in range(height):
        for x in range(width):
            seen.add((x, y))
            color = image.getpixel((x, y))
            if color == FILL_COLOR:
                color = None
            else:
                x_real_min = min(x_real_min, x)
                y_real_min = min(y_real_min, y)
                x_real_max = max(x_real_max, x)
                y_real_max = max(y_real_max, y)
            pixels[y].append(color)

    return serialize(
        pixels,
        x_real_min,
        x_real_max,
        y_real_min,
        y_real_max,
        debug,
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        '--file', type=str, 
        help='the file where the sum should be written')
    parser.add_argument(
        '--debug', action='store_true', default=False,
        help='debug')
    args = parser.parse_args()
    assert os.path.exists(args.file)


    result = convert_image(args.file, args.debug)
    print(result)
