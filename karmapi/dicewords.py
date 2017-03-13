""" 
Word list from diceware.
"""


def load(infile):

    words = ''
    six = set([str(x) for x in range(1, 7)])
    for row in intfile:
        if row[0] in six:
            words.append(row.split()[-1])

    return words
