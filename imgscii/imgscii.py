"""This program is used to print ASCII art to the console.

Usage
-----

    $ python imgscii.py
"""

import os.path as path
import argparse

from PIL import Image
from colorama import init, Fore
import colorsys

ASCII_CHARS = ("#", "?", "%", "$", "Q", "+", ",", "j", "*", "~", "`", ".")


def main():
    """Accept user input and use the provided information to open an image
    and create an ASCII representation.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--columns", type=int,
                        help="Define the width of ASCII art in columns.")
    args = parser.parse_args()

    file_name = input("What is the name of the image?\n")

    while not path.isfile(file_name):
        print("Could not open image: '{}'".format(file_name))
        file_name = input("What is the name of the image?\n")

    while True:
        if args.columns:
            columns = int(args.columns)
            break

        columns = input("How many columns do you want your ASCII art to be?\n")

        # Ensure input is a positive float or integer
        try:
            columns = int(columns)
            if columns > 0:
                break
            else:
                print("Please enter a whole number. Example: 30")
                continue
        except ValueError:
            print("Please enter a whole number. Example: 30")
            continue

    printscii(file_name, columns=columns)


def display_ascii(ascii_list):
    """Prints the contents of a list.

    Parameters
    ----------
    ascii_list : list

    """

    init()  # Initialize Colorama

    print(*ascii_list, sep="")


def resize_image(img, new_width=60):
    """Resize an image opened via PIL's Image.open().

    Maintains aspect ratio.

    Parameters
    ----------
    img : object
    new_width : int

    Returns
    -------
    object
        A PIL Image

    """

    original_width, original_height = img.size

    # Get scale factor of output img and use it to calculate the output height
    scale = new_width / original_width
    new_height = original_height * scale

    return img.resize((round(new_width), round(new_height)))


def read_pixel_data(img, width=60, char_set=ASCII_CHARS):
    """Iterates through pixels in a PIL.Image.

    Each pixel's color and luminance values are calculated and a list of
    ASCII characters is created.

    Parameters
    ----------
    img : object
    width : int
    char_set : tuple

    Returns
    -------
    list
        A list of ASCII characters.
    """

    if not isinstance(char_set, tuple):
        raise TypeError("char_set must be of type tuple.")

    pixels = list(img.getdata())
    ascii_pixels = []
    i = 0

    for pixel in pixels:
        # Use pixel luminance to determine the ASCII character used.
        lum = get_luminance(pixel)
        index = round((len(char_set) - 1) * lum)

        color = get_color(pixel)

        # ANSI escape code is paired w/ an ASCII char to produce a styled char
        ascii_pixels.append(color + char_set[index])

        # Add a newline after ever I iterations, where I is the output width
        if i == width - 1:
            ascii_pixels.append("\n")
            i = 0
        else:
            i += 1

    return ascii_pixels


def get_luminance(pixel):
    """Use the pixels RGB values to calculate its luminance.

    Parameters
    -----------
    pixel : tuple

    Returns
    -------
    float
        Value is between 1.0 and 0.0
    """

    luminance = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
    luminance /= 255

    return round(luminance, 2)


def get_color(pixel):
    """Get the color of a pixel and return the ANSI escape code.

    https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

    Parameters
    -----------
    pixel : tuple

    Returns
    -------
    str
        An ANSI escape code.
     """

    # By slicing the tuple we are able to ignore the alpha channel if it exists
    red, green, blue = pixel[:3]

    # Convert RGB values to floats. 255 => 1.0
    red /= 255
    green /= 255
    blue /= 255

    hue, lum = colorsys.rgb_to_hls(red, green, blue)[:2]

    # Convert hue to range of 0 to 360 degrees
    hue *= 360

    if lum >= 0.7:
        color_code = Fore.WHITE  # ANSI fg white
    elif lum <= 0.2:
        color_code = Fore.BLACK  # ANSI fg black
    else:
        if 30 < hue <= 90:
            color_code = Fore.YELLOW  # ANSI fg yellow
        elif 90 < hue <= 150:
            color_code = Fore.GREEN  # ANSI fg green
        elif 150 < hue <= 210:
            color_code = Fore.CYAN  # ANSI fg cyan
        elif 210 < hue <= 270:
            color_code = Fore.BLUE  # ANSI fg blue
        elif 270 < hue <= 330:
            color_code = Fore.MAGENTA  # ANSI fg magenta
        else:  # hue <= 30 or hue > 330
            color_code = Fore.RED  # ANSI fg red

    return color_code


def printscii(file, **kwargs):
    """Open an image and print it's contents to the console as ASCII art.

    Parameters
    -----------
    file : str
    columns : int
    char_set : list

    Returns
    -------
    None

     """

    width = kwargs.get("columns", 60)
    characters = kwargs.get("char_set", ASCII_CHARS)

    try:
        with Image.open(file) as image:
            image = resize_image(image, width)
            ascii_image = read_pixel_data(image, width, characters)
            display_ascii(ascii_image)
    except OSError as error:
        print(error)


if __name__ == "__main__":
    main()
