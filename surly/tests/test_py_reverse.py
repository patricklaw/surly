import unittest

from surly.re_parse import reverse_template

class JSTestCase(unittest.TestCase):
    def test_py_simple(self):
        value = reverse_template(r'a')
        assert value == 'a', value
    