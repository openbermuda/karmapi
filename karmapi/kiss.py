"""
Kiss goodbye to data

hello, just the same

exceptions and all sorts of complications

keep it simple

share
"""
from karmapi import checksum, base

from curio import run, tcp_server


async def goodbye(data, **meta)
    """ kiss good-bye to data """

    ck = checksum.checksum(data)

    # check meta data etc -- see checksum module

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



async def echo_client(client, addr):
    print('Connection from', addr)
    s = client.as_stream()
    async for line in s:
        await s.write(line)
    print('Connection closed')
    await s.close()


if __name__ == '__main__':
    try:
        run(tcp_server, '', 25000, echo_client)
    except KeyboardInterrupt:
        pass
