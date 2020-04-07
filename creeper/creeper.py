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
            return

# exemple : setpixel(60,60,'ffffff')

def drawCreeper(x, y):
    for i in range(10): #ligne 1
        setpixel(x+i,y, '00ff00')
    #setpixel(x+9,y, '00ff00')
    print('ligne 1')
    
    for i in range(10): #ligne 2
        setpixel(x+i,y+1, '00ff00')
    print('ligne 2')
    
    #ligne 3
    setpixel(x,y+2, '00ff00')
    setpixel(x+1,y+2, '00ff00') 
    setpixel(x+2,y+2, '000000') 
    setpixel(x+3,y+2, '000000') 
    setpixel(x+4,y+2, '00ff00') 
    setpixel(x+5,y+2, '00ff00')
    setpixel(x+6,y+2, '000000') 
    setpixel(x+7,y+2, '000000') 
    setpixel(x+8,y+2, '00ff00') 
    setpixel(x+9,y+2, '00ff00')
    print('ligne 3')
    
    #ligne 4
    setpixel(x,y+3, '00ff00')
    setpixel(x+1,y+3, '00ff00') 
    setpixel(x+2,y+3, '000000') 
    setpixel(x+3,y+3, '000000') 
    setpixel(x+4,y+3, '00ff00') 
    setpixel(x+5,y+3, '00ff00')
    setpixel(x+6,y+3, '000000') 
    setpixel(x+7,y+3, '000000') 
    setpixel(x+8,y+3, '00ff00') 
    setpixel(x+9,y+3, '00ff00')
    print('ligne 4')

    #ligne 5
    for i in range(4):
        setpixel(x+i,y+4, '00ff00')
    setpixel(x+4,y+4, '000000')
    setpixel(x+5,y+4, '000000')    
    for i in range(4):
        setpixel(x+i+6,y+4, '00ff00')
    print('ligne 5')
    
    #ligne 6
    for i in range(3):
        setpixel(x+i,y+5, '00ff00')
    setpixel(x+3,y+5, '000000')
    setpixel(x+4,y+5, '000000')
    setpixel(x+5,y+5, '000000')    
    setpixel(x+6,y+5, '000000')    
    for i in range(3):
        setpixel(x+i+7,y+5, '00ff00')
    print('ligne 6')
    
    #ligne 7
    for i in range(3):
        setpixel(x+i,y+6, '00ff00')
    setpixel(x+3,y+6, '000000')
    setpixel(x+4,y+6, '000000')
    setpixel(x+5,y+6, '000000')    
    setpixel(x+6,y+6, '000000')    
    for i in range(3):
        setpixel(x+i+7,y+6, '00ff00')
    print('ligne 7')
    
    #ligne 8
    for i in range(10):
        if(i == 3 or i == 6):
            setpixel(x+i, y+7, '000000')
        else:
            setpixel(x+i, y+7, '00ff00')
    print('ligne 8')
    
    for i in range(10): #ligne 9
        setpixel(x+i,y+8, '00ff00')  
    print('ligne 9')
    
    for i in range(10): #ligne 10
        setpixel(x+i,y+9, '00ff00')
    print('ligne 10')

drawCreeper(1,25)
print("ok")
