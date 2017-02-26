""" Tests for primes 

If you have an idea about primes you can test it here.

"""

import unittest

import hypothesis


from karmapi import primes

class Prime(unittest.TestCase):


    def test_isprime(self):


        self.assertEqual(
            primes.isprime(2), isprime(2))

        
