"""
Simple substitution

The Babington Plot according to wiki pedya::

    https://en.wikipedia.org/wiki/Babington_Plot

Simon Singh has a book on the history of crytography.

Will see if I can find one.

My Queen Mary went with as simple substitution + some magic codes.

But I'm not sure the magic works, even in python.  It's a human thing.

So, here's a simple sub with a twist for now.

"""

def key_to_alpha(key):
    """ Generate alphabet for key 

    Idea is run through the key, dropping any 
    letters already seen.
 
    Then go back to the beginning of the alphabet and 
    write letters out that are not in the key.
    """
    alphabet = ''
    used = set()

    for c in key:
        if c.lower() not in used:
            alphabet += c
            used.add(c)

    a = ord('a')

    for xx in range(26):
        c = chr(a + xx)
        if c not in used:
            alphabet += c

    return alphabet

def gen_cipher_lookup(alpha, didigs=None):

    didigs = didigs or [1, 2]

    available = [x for x in range(10) if x not in didigs]
    print(available)
    
    calpha = [str(x) for x in available]
    for digit in didigs:
        for x in available:
            calpha.append(str((10 * digit) + x))

    lookup = {}
    for p, c in zip(alpha, calpha):
        lookup[p] = c

    return lookup
        
    
def encode(message, cipher):

    result = ''
    for c in message:
        code = cipher.get(c, c)
        result += code

    return result


import argparse
import sys


parser = argparse.ArgumentParser()

parser.add_argument('--key', default='iloveyou')
parser.add_argument('--mj', action='store_true')
parser.add_argument('--cheat', action='store_true')

args = parser.parse_args()


message = sys.stdin.read()

alpha = key_to_alpha(args.key)

cipher = gen_cipher_lookup(alpha)

if args.mj:
    print("Not yet implemented :(")
    sys.exit(26)

if args.cheat:
    for p, c in cipher.items():
        print(p, c)
        
print(encode(message, cipher))

