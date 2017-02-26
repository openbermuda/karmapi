""" Tests for primes 

If you have an idea about primes you can test it here.

"""

import unittest

import hypothesis


from karmapi import prime

class Prime(unittest.TestCase):


    def _test_isprime(self):

        # FIXME find elsewhere
        from elsewhere import isprime

        self.assertEqual(
            prime.isprime(2), isprime(2))

    def test_is2prime(self):


        self.assertEqual(
            prime.isprime(2), True)

        
