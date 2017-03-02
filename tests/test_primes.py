""" Tests for primes 

If you have an idea about primes you can test it here.

"""

import unittest

from hypothesis import given

from hypothesis.strategies import integers


from karmapi import prime


PRIMES = set([2, 3, 5, 7, 11, 13, 17, 19, 23])

def isprime(n):
    """ In lieu of somebody else solving this problem 

    Returns True if n is prime
    
    Returns False if n is not prime.

    Return None if not sure. Currently, not sure if n > 23.
    """

    maxp = max(PRIMES)

    if n > maxp:
        return None
        
    if n in PRIMES:
        return True

    return False

class Prime(unittest.TestCase):


    def _test_isprime(self):

        self.assertEqual(
            prime.isprime(2), isprime(2))

    def test_is2prime(self):


        self.assertEqual(
            prime.isprime(2), True)


    @given(integers(min_value=2, max_value=10000))
    def test_isnprime(self, n):

        is_it_prime = isprime(n)

        karma_prime = prime.isprime(n)
        
        if is_it_prime != None:
            # if isprime knows, check it agrees with our version
        
            assert(is_it_prime == karma_prime)
        
