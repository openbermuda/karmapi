"""

"""

from collections import defaultdict

def matcher(a, b):
    """ Find things in a that match things in b 

    Args:

       a: list of dictionaries to match
       b: list of dictionaries to find matches for
    """

    result = defaultdict(list)

    for bx, item in enumerate(b):
        for ax, target in enumerate(a):

            bkeys = set(item.keys())
            akeys = set(target.keys())

            # if b has keys not in a, then not a match
            if not bkeys.issubset(akeys): continue

            hit = True
            for k in item:

                # if values don't match, not a match
                if item[k] != target[k]:
                    hit = False
                    break

            if hit:
                result[bx].append(target)

    # For each match, find the size of each match.
    # Then keep just the smallest matches
    keep = []

    for ix, hits in result.items():
        sizes = [len(x) for x in hits]
        minsize = min(sizes)
        
        keepers = [x for x in hits if len(x) == minsize]
    
        keep.append((a[ix], keepers))

    return keep
