"""
Kiss goodbye to data

hello, just the same

exceptions and all sorts of complications

keep it simple

share
"""
import argparse

from karmapi import checksum, base

from curio import run, tcp_server

PORT = 8008

async def goodbye(data, **meta):
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


async def client(host, port):
    sock = await curio.open_connection(
        host, port)
    async with sock:
        await sock.sendall(b'kiss\r\nWOW HERE I AM\r\n\r\n')
        chunks = []
        while True:
            chunk = await sock.recv(10000)
            if not chunk:
                break
            chunks.append(chunk)

    response = b''.join(chunks)
    print(response.decode('latin-1'))
    
    

def get_parser():

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=PORT)
    parser.add_argument('--serve', action='store_true')

    return parser


if __name__ == '__main__':

    parser = get_parser()

    args = parser.parse_args()

    if args.serve:
        try:
            run(tcp_server, args.host, args.port, echo_client)
        except KeyboardInterrupt:
            pass

    else:
        # client mode
        run(client, args.host, args.port)
