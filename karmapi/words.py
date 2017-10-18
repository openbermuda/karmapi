"""  count words
"""

from collections import Counter

from pathlib import Path

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('path', nargs='+')

parser.add_argument('--glob', default='**/*.rst')

args = parser.parse_args()


totals = Counter()

for path in args.path:
    print(path)
    for name in Path(path).glob(args.glob):

        print(name)

        counts = Counter()

        counts.update(name.open().read().split())

        print(counts.most_common(7))
        print(sum(counts.values()))
        print()

        totals.update(counts)

print('Totals:')

print(totals.most_common(26))

print(sum(totals.values()))
        
