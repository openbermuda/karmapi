import unittest


class TestNullCode(unittest.TestCase):


    def test_null_code(self):

        with self.assertRaises(ValueError) as cm:

            import null_code


        error = cm.exception
        assert(str(error) == 'source code string cannot contain null bytes')

