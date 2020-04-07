import sys, requests
from PIL import Image
from fetch_pixelwar_image import fetch_pixelwar_image
from proofs import proofs

def set_pixel(x, y, color, proof):
    params = {
        'x': str(x),
        'y': str(y),
        'color': color,
        'proof': proof
    }
    r = requests.get('http://137.74.47.86/setpixel', params=params)
    return r

def pixel_dist1(p1, p2):
    return abs(p1[0]- p2[0]) + abs(p1[1]- p2[1]) + abs(p1[2]- p2[2])

def pixel_dist(p1, p2):
    return max(abs(p1[0]- p2[0]), abs(p1[1]- p2[1]), abs(p1[2]- p2[2]))

img = Image.open('codingame_100.png').convert('RGB')
img_width, img_height = img.size
pixels = img.load()

pixelwar_img = fetch_pixelwar_image()
pixelwar_pixels = pixelwar_img.load()

proof_index = 0
diffs = 0

for y in range(img_height):
    for x in range(img_width):
        # ignore salamèche:
        if 24 <= x < 44 and 4 <= y < 24:
            continue
        # ignore isabelle/space invaders:
        if 30 <= x < 55 and 65 <= y < 89:
            continue
        # ignore bottom-right corner:
        if 80 <= x < 100 and 80 <= y < 100:
            continue
        # ignore top-left corner:
        if 0 <= x < 25 and 0 <= y < 25:
            continue
        # ignore top-right corner:
        if 79 <= x < 100 and 0 <= y < 21:
            continue
        # actual_x, actual_y = x + 34, y + 68
        # actual_x, actual_y = x + 68, y + 68
        actual_x, actual_y = x, y
        pixel = pixels[x, y]
        pixelwar_pixel = pixelwar_pixels[actual_x, actual_y]
        if pixelwar_pixel == pixel:
            continue

        # grattage de quelques hashs: ignorer les pixels proches
        d = pixel_dist(pixel, pixelwar_pixel)
        if d <= 100:
            continue

        # print(f'difference at {actual_x}, {actual_y}: {pixelwar_pixel}')
        diffs += 1
        color = '%02x%02x%02x' % pixel

        success = False
        while not success:
            proof = proofs[proof_index]
            print(f'Trying {actual_x},{actual_y}   #{color}   {proof}')
            r = set_pixel(actual_x, actual_y, color, proof)
            # if r.text.strip() == 'Proof already used':
            success = r.status_code == 200
            proof_index += 1

print(diffs)

print(f'proof_index={proof_index}  last_proof={proof}')
