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

    while True:
        file_name = input("What is the name of the image?\n")

        # Check input for empty string
        if not file_name:
            print("Please enter a filename.")
            continue

        try:
            image = Image.open(file_name)
            break
        except IOError:
            print("Could not open image: '{}'".format(file_name))

    while True:
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


def read_pixel_data(img, width=60):
    """Iterates through pixels in a PIL.Image.

    Each pixel's color and luminance values are calculated and a list of
    ASCII characters is created.

    Parameters
    ----------
    img : object
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
        # Use pixel luminance to determine the ASCII character used.
        lum = get_luminance(pixel)
        index = round((len(ascii_chars) - 1) * lum)

        # Color is converted from RGB to ANSI color code
        color = get_color(pixel)
        char = hues.huestr(ascii_chars[index], hue_stack=(color,)).colorized

        # Colorized Hue string is appended to list
        ascii_pixels.append(char)

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
    int
        An ANSI escape code.
     """

    # By slicing the tuple we are able to ignore the alpha channel if it exists
    red, green, blue = pixel[:3]

    # Convert RGB values to floats. 255 => 1.0
    red /= 255
    green /= 255
    blue /= 255

    hue, lum, sat = colorsys.rgb_to_hls(red, green, blue)

    # Convert hue to range of 0 to 360 degrees
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
