# Imgscii
Imgscii is a simple program that converts images into ASCII artwork. Follow the prompts and your ASCII art will be printed to your console. I plan on adding more features and improvements in the future.

## Getting Started
You can get started by installing Imgscii using PIP:

```
pip install imgscii
```

## Usage
### As A Module
After you have installed the package from PIP you can import Imgscii into your project.

```
import imgscii

imgscii.printscii("images/my-photo.jpg")
```

Imgscii currently supports a small set of keyword arguments.

**monochrome**: ASCII art will be printed with default console style... no color!
```
imgscii.printscii("images/my-photo.jpg", monochrome=True)
```

**columns**: Define the width of your ASCII art in columns. Aspect ratio will be maintained.
```
imgscii.printscii("images/my-photo.jpg", columns=75)
```

**char_set**: Provide your own character set.
```
imgscii.printscii("images/my-photo.jpg", char_set=("#", "$", "Q", "v", "j", ";", "."))
```

### From The Console
Imgscii can be executed from the console as well. Use `cd` to navigate to the directory containing
`imgscii.py`and run the program with the following command:

```
python imgscii.py
```

You can also use command line arguments.

**-m, --monochrome**: Print ASCII art without colors
**-c, --columns**: Define the width of ASCII art in columns.

## To-Dos
* Add more options for printing
* Create more ASCII artwork
