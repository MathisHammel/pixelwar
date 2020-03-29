import random, hashlib, requests
from itertools import product

# Better version in Java:
# see hash-cracker\src\main\java\App.java

f = open("proofs_python.txt", "w")

prefix = '255'

for p in product('h25io', repeat=30 - len(prefix)):
    proof = prefix + ''.join(p)
    if hashlib.sha256(('h25' + ''.join(proof)).encode()).hexdigest().startswith('00000'):
        print(proof)
        f.write(proof)
        f.write('\n')
        f.flush()

f.close()
