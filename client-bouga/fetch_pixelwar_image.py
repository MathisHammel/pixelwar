import sys, random, hashlib, requests
from PIL import Image

local_image_file = 'pixelwar.png'

def fetch_pixelwar_image():
    response = requests.get('http://137.74.47.86/image')

    if response.status_code != 200:
        raise Exception('Cant download image from server')

    with open(local_image_file, 'wb') as f:
        f.write(response.content)

    img = Image.open(local_image_file).convert('RGB')
    return img

if __name__ == '__main__':
    img = fetch_pixelwar_image()
    pixels = img.load()
    print(pixels[0,0])
