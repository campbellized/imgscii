from PIL import Image

def displayASCII(ascii_list):
    """
    Prints a list of characters
    """

    print(*ascii_list, sep="")
    
def displayImage(img):
    """
    Display an image
    """
    
    img.show()
    
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
    
    pixels = list(img.getdata())
    ascii_pixels = []
    i = 0
    
    for p in pixels:
        # Char is assigned by pixel luminance
        lum = getLuminance(p)
        index = round((len(ASCII_CHARS) - 1) * lum)        
        ascii_pixels.append(ASCII_CHARS[index])
        
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

ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

file_name = input("What is the name of the image?\n")
columns = input("How many columns do you want your ASCII to be?\n")
columns = int(columns)

image = ""

try:
    image = Image.open(file_name)
except IOError:
    print("Could not open image: '{}'".format(file_name))
finally:
    if(image):
        image = resizeImage(image, columns)
        ascii_image = readPixelData(image, columns)
        displayASCII(ascii_image)
#        displayImage(image)
        image.close()