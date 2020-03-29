import random
import hashlib
import requests
from PIL import Image
from time import sleep
from multiprocessing import Process, Manager
import os
from urllib.parse import quote


# Ouvre notre logo
img = Image.open('fond3.png')
img = img.convert('RGB').resize((25,25))
w, h = img.size
print(img.size)

data = img.getdata()

manager = Manager()
proofs = manager.list()


# Trouve des proofs dans /dev/urandom
def find_proofs():
    while True:
        proof = ""
        while not hashlib.sha256(('h25'+proof).encode()).hexdigest().startswith('00000'):
            proof = str(os.urandom(10))
        if proof not in proofs:
            proofs.append(proof)
            print(len(proofs), "/", int(w*h*1.2), proof)


# Lance le process sur 20 coeurs
for _ in range(20):
    Process(target=find_proofs).start()


# La fonction qu'on aime
def setpixel(x, y, color):
    params = {'x': str(x),
              'y': str(y),
              'color': color,
              'proof': proofs.pop()}
    r = requests.get('http://137.74.47.86/setpixel', params=params)
    print(r.text)
    return r.text


# Dés qu'on a des proofs on dessine
i = 0
while True:
    if len(proofs) > 0:
        x = i % w
        y = i // w
        r, g, b = data[i]
        color = hex(r*0x10000+g*0x100+b)[2:]
        color = "0"*(6-len(color)) + color
        print(color, x, y)
        r = setpixel(x, y, color)
        if "OK" in r:
            i += 1
            i %= h*w
        sleep(0.05)
