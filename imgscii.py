"""This program is used to print ASCII art to the console.

Usage
-----

    $ python imgscii.py
"""

from PIL import Image
import hues
import colorsys


def main():
    """Accept user input and use the provided information to open an image
    and create an ASCII representation.
    """
    image = ""
    file_name = input("What is the name of the image?\n")

    while not image:
        try:
            image = Image.open(file_name)
            break
        except IOError:
            print("Could not open image: '{}'".format(file_name))
            file_name = input("What is the name of the image?\n")

    columns = input("How many columns do you want your ASCII art to be?\n")

    while not isinstance(columns, int):
        try:
            columns = int(columns)
            if columns <= 0:
                columns = input("Please enter an whole number.\n")
                continue
            else:
                break
        except ValueError:
            columns = input("Please enter an whole number.\n")

    image = resize_image(image, columns)
    ascii_image = read_pixel_data(image, columns)
    display_ascii(ascii_image)
    image.close()


def display_ascii(ascii_list):
    """Prints the contents of a list.

    Parameters
    ----------
    ascii_list : list

    """

    print(*ascii_list, sep="")


def resize_image(img, new_width=60):
    """Resize an image opened via PIL's Image.open().

    Maintains aspect ratio.

    Parameters
    ----------
    img : PIL Image
    new_width : int

    Returns
    -------
    PIL Image

    """

    # Get original dimensions and aspect ratio
    (original_width, original_height) = img.size

    # Calculate scale of new dimensions relative to original
    scale = (new_width * 100) / original_width
    scale *= 10**-2

    # Calculate new dimensions
    new_width = original_width * scale
    new_height = original_height * scale

    return img.resize((round(new_width), round(new_height)))


def read_pixel_data(img, width=60):
    """Iterates through pixels in a PIL.Image.

    Each pixel's color and luminance values are calculated and a list of
    ASCII characters is created.

    Parameters
    ----------
    img : PIL Image
    width : int

    Returns
    -------
    list
        A list of ASCII characters.
    """
    ascii_chars = ["#", "?", "%", "$", "Q", "+", ",", "j", "*", "~", "`", "."]

    pixels = list(img.getdata())
    ascii_pixels = []
    i = 0

    for pixel in pixels:
        # Char is assigned by pixel luminance
        lum = get_luminance(pixel)
        index = round((len(ascii_chars) - 1) * lum)

        # Color is  converted from RGB to ANSI color code
        color = get_color(pixel)
        char = hues.huestr(ascii_chars[index], hue_stack=(color,)).colorized

        # Colorized Hue string is appended to list
        ascii_pixels.append(char)

        # Add newlines as necessary
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
    int
        An ANSI escape code.
     """

    (red, green, blue) = pixel

    # Convert RGB values to floats. 255 => 1.0
    red /= 255
    green /= 255
    blue /= 255

    # Convert hue to range of 0 to 360 degrees
    (hue, lum, sat) = colorsys.rgb_to_hls(red, green, blue)
    hue *= 360

    if lum >= 0.7:
        color_code = 37  # ANSI fg white
    elif lum <= 0.2:
        color_code = 30  # ANSI fg black
    else:
        if 30 < hue <= 90:
            color_code = 33  # ANSI fg yellow
        elif 90 < hue <= 150:
            color_code = 32  # ANSI fg green
        elif 150 < hue <= 210:
            color_code = 36  # ANSI fg cyan
        elif 210 < hue <= 270:
            color_code = 34  # ANSI fg blue
        elif 270 < hue <= 330:
            color_code = 35  # ANSI fg magenta
        else:  # hue <= 30 or hue > 330
            color_code = 31  # ANSI fg red

    return color_code

if __name__ == "__main__":
    main()
