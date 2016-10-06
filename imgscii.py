from PIL import Image
import hues
import colorsys


def main():    
    image = ""
    file_name = ""
    columns = None
    
    file_name = input("What is the name of the image?\n")
    
    while not image:
        try:
            image = Image.open(file_name)
            break
        except IOError:
            print("Could not open image: '{}'".format(file_name))
            file_name = input("What is the name of the image?\n")
    
    columns = input("How many columns do you want your ASCII art to be?\n")
    
    while type(columns) != "int":    
        try:
            columns = int(columns)
            if columns <= 0:
                columns = input("Please enter an whole number.\n")
                continue
            else:           
                break
        except ValueError:
            columns = input("Please enter an whole number.\n")
    
    image = resizeImage(image, columns)
    ascii_image = readPixelData(image, columns)
    displayASCII(ascii_image)
    image.close()
    

def displayASCII(ascii_list):
    """
    Prints a list of characters
    """

    print(*ascii_list, sep="")


def resizeImage(img, new_width=60):
    """
    Resize an image, maintaining its aspect ratio
    """

    # Get original dimensions and aspect ratio
    (original_width, original_height) = img.size

    # Calculate scale of new dimensions relative to original
    scale = (new_width * 100) / original_width
    scale = scale * 10**-2

    # Calculate new dimensions
    new_width = original_width * scale
    new_height = original_height * scale

    return img.resize((round(new_width), round(new_height)))


def readPixelData(img, width=60):
    """
    Iterates through pixels in a PIL.Image. Returns list of ASCII characters.
    """
    ascii_chars = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]
    
    pixels = list(img.getdata())
    ascii_pixels = []
    i = 0

    for p in pixels:
        # Char is assigned by pixel luminance
        lum = getLuminance(p)
        index = round((len(ascii_chars) - 1) * lum)

        # Color is  converted from RGB to ANSI color code
        color = getColor(p)
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


def getLuminance(pixel):
    """
    Calculate the luminance value using RGB
    """

    luminance = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
    luminance = luminance / 255

    return round(luminance, 2)


def getColor(pixel):
    """
    Calculates the color of a pixel and returns the ANSI color code
    """

    (r, g, b) = pixel

    # Convert RGB values to floats. 255 => 1.0
    r = r / 255
    g = g / 255
    b = b / 255

    # Convert hue to range of 0 to 360 degrees
    (h, l, s) = colorsys.rgb_to_hls(r, g, b)
    h = h * 360

    if l >= 0.7:
        return 37 # ANSI fg white
    if l <= 0.2:
        return 30 # ANSI fg black
    if h <= 30 or h > 330:
        return 31 # ANSI fg red
    if h > 30 and h <= 90:
        return 33 # ANSI fg yellow
    if h > 90 and h <= 150:
        return 32 # ANSI fg green
    if h > 150 and h <= 210:
        return 36 # ANSI fg cyan
    if h > 210 and h <= 270:
        return 34 # ANSI fg blue
    if h > 270 and h <= 330:
        return 35 # ANSI fg magenta

if __name__ == "__main__":
    main()