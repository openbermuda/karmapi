

names = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'c2']
#toc =   [1,  9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2]

notes = {'f': 1.3333333333333333, 'e': 1.25, 'c': 1, 'b': 1.875, 'g': 1.5, 'd': 1.125, 'a': 1.6666666666666667, 'c2': 2}


def beat(a, b):
    """ Figure out beat frequency between a pair of notes """
    
    aa = notes[a]
    bb = notes[b]

    form = '{:3} {:3}' + '{:4.0f} ' * 2
    ratio = bb / aa
    for x in range(1, 100):
        if ((x * ratio) - int(x * ratio)) < 0.0001:
            print(form.format(a, b, x, x * ratio))
            break

def whole(x, thresh=1e-6):

    return (x - int(x)) < thresh
        
def beat2(a, b):
    """ Figure out beat frequency between a pair of notes """
    
    aa = notes[a]
    bb = notes[b]

    form = '{:3} {:3}' + '{:4.0f} ' * 3
    #ratio = bb / aa
    for x in range(1, 100):

        ax = x * aa
        bx = x * bb

        if whole(ax) and whole(bx):

            print(form.format(a, b, x, ax, bx))
            break

        
if __name__ == '__main__':

    for ix in range(len(names)):
        for jx in range(ix+1, len(names)):
            beat2(names[ix], names[jx])
        print()
