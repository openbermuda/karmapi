import curio

from karmapi.gilliam import terry

def func():

    assert not terry()

async def coro():

    assert terry()

func()
    
xx = curio.run(coro)

