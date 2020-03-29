from flask import Flask, request, send_file
from flask_api import status
from io import BytesIO
from PIL import Image
import redis
import hashlib
import time

red = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/image')
def image():
    if not red.exists('imgttl') or time.time() - int(red.get('imgttl')) > 60:
        im = Image.new('RGB', (100, 100))
        for x in range(100):
            for y in range(100):
                color = 'ff9900'
                if red.exists(f'pixel:{x}:{y}'):
                    color = red.get(f'pixel:{x}:{y}')
                r,g,b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
                im.putpixel((x, y), (r, g, b))
        im.save('cached.png')
        red.set('imgttl', int(time.time()))
        return serve_pil_image(im)
    else:
        im = Image.open('cached.png')
        return serve_pil_image(im)

@app.route('/')
def root():
    return '''<html>
    <head>
        <meta http-equiv="refresh" content="60">
    </head>
    <body>
        <img src="/image" />
    </body>
    <br><br><br>
    <a href="/about">About</a>
</html>'''

@app.route('/setpixel')
def setpixel():
    args = request.args
    for arg in ('x', 'y', 'color', 'proof'):
        if arg not in args:
            return 'Missing query param ' + arg, status.HTTP_400_BAD_REQUEST 
    proof = args['proof']
    if not hashlib.sha256(('h25'+proof).encode()).hexdigest().startswith('00000'):
        return 'Invalid proof', status.HTTP_401_UNAUTHORIZED
    if red.exists('proof:'+proof):
        return 'Proof already used', status.HTTP_401_UNAUTHORIZED

    x = int(args['x'])
    y = int(args['y'])
    color = args['color']

    if not 0 <= x <= 99 or not 0 <= y <= 99:
        return 'Pixel out of range', status.HTTP_400_BAD_REQUEST
    
    if not (len(color) == 6 and all(c in '0123456789abcdef' for c in color)):
        return 'Invalid color (has to be /[0-9a-f]{6}/)', status.HTTP_400_BAD_REQUEST

    red.set('proof:'+proof, 'used')
    red.set(f'pixel:{x}:{y}', color)
    return 'OK', status.HTTP_200_OK

@app.route('/about')
def about():
    return '''<html>Ce site est une experience pour le stream de la quarantaine disponible <a href="https://live.h25.io">ici</a>.
<br><br>
Vous pouvez changer un pixel de votre choix en envoyant une requete GET sur l'endpoint /setpixel?x=...&y=...&color=...&proof=...
<br><br>
x et y sont compris entre 0 et 99 (le coin en haut a gauche est (0,0))<br>
color est une string hex representant la couleur, par exemple ff9900<br>
proof est une preuve de travail telle que SHA256("h25" + proof) commence par 00000. <br>
<br>
Exemple de client (Python3) : <br>
<pre>
import random, hashlib, requests

def setpixel(x,y,color):
    while True:
        proof = ''.join([random.choice('h25io') for _ in range(30)])
        if hashlib.sha256(('h25'+proof).encode()).hexdigest().startswith('00000'):
            params = {'x':str(x),
                      'y':str(y),
                      'color':color,
                      'proof':proof}
            r = requests.get('http://137.74.47.86/setpixel', params=params)
            print(r.text)

# exemple : setpixel(60,60,'ffffff')
</pre>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
