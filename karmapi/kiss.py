"""
Kiss goodbye to data

hello, just the same

exceptions and all sorts of complications

keep it simple

share
"""
from karmapi import checksum, base

from curio import Q

history

async def goodbye(data, **meta)
    """ kiss good-bye to data """

    ck = checksum.checksum(data)

    path = meta.getdefault('path', base.Path('.'))

    # any matches?  Somebody else's problem?
    #     run delta for each match?
    
    # save a copy?
    if not path.exists():
        save(data, path)
    # vision test?  Looks the same?  How to?

    # 2018 aeh eye

    # catch exceptions?


hello = goodbye
