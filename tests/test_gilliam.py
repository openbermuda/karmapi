import curio

from karmapi.gilliam import terry


async def coro():

    for x in range(10):
        await curio.sleep(.1)
        print(x)
        
    
    print('CORO terry():', terry())

    assert terry() == False


xx = curio.run(coro)

print(xx)
