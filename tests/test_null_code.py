import unittest


class TestNullCode(unittest.TestCase):


    def test_null_code(self):

        try:

            from . import null_code

        except ValueError as error:
            print(error)

            raise(error)
