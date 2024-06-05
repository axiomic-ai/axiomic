
from PIL import Image
from io import BytesIO
import requests
from rich.console import Console
import base64



class AImage:
    '''
    A container for a PIL Image with quality of life functions.
    
    Named to avoid conflict with the PIL Image class.

    TODO: WIP. Under construction.
    '''
    def __init__(self, img: Image):
        self.img = img

    def print(self, width=None):
        if width is None:
            console = Console()
            width, _ = console.size
        ansi = image_to_ansi(self.img, max_width=width)
        print(ansi)
        return self

    def __str__(self):
        return image_to_ansi(self.img, max_width=40)

    def save(self, path: str):
        self.img.save(path)


def image_from_base64(base64_str: str) -> Image:
    image_data = base64.b64decode(base64_str)
    image_data = BytesIO(image_data)
    image = Image.open(image_data)
    return AImage(image)


def image_from_url(url: str) -> Image:
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return AImage(image)


def image_to_ansi(img: Image, max_width=120, aspect_ratio=0.503):  # aspect_ratio adjusted for typical terminal character dimensions
    img = img.resize((max_width, int(max_width * img.height / img.width * aspect_ratio)))
    img = img.convert('RGB')
    
    ansi_image = ""
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            ansi_image += f"\x1b[48;2;{pixel[0]};{pixel[1]};{pixel[2]}m "  # Color the background
        ansi_image += '\x1b[0m\n'  # Reset the color at the end of each line
    
    return ansi_image