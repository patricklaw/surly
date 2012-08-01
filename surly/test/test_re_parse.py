import unittest

from surly.re_parse import reverse, ReverseParseError
import sre_constants


class ReverseTestCase(unittest.TestCase):
    special_sequences = [
        (r'^', {}, u''),
        (r'$', {}, u''),
        (r'\A', {}, ReverseParseError),
        (r'\B', {}, ReverseParseError),
        (r'\d', {}, ReverseParseError),
        (r'\D', {}, ReverseParseError),
        (r'\s', {}, ReverseParseError),
        (r'\S', {}, ReverseParseError),
        (r'\w', {}, ReverseParseError),
        (r'\W', {}, ReverseParseError),
        (r'\Z', {}, ReverseParseError),
        (r'\a', {}, u'\a'),
        (r'\b', {}, ReverseParseError),
        (r'\f', {}, u'\f'),
        (r'\n', {}, u'\n'),
        (r'\r', {}, u'\r'),
        (r'\t', {}, u'\t'),
        (r'\v', {}, u'\v'),
        (r'\\', {}, u'\\'),
    ]

    capture_groups = [
        # A very simple named capture
        (r'(?P<cap1>a)',
         {'cap1': 'cap1_val'},
         u'cap1_val'),

        # A named capture nested within a non-capturing group
        (r'(?:(?P<cap1>.))',
         {'cap1': 'cap1_val'},
         u'cap1_val'),

        # A capture explicitly mentioned twice (should return an error)
        (r'(?P<cap1>.)(?P<cap1>.)',
         {'cap1': 'cap1_val'},
         sre_constants.error),

        # Repeats are not supported outside of named captures
        (r'(?P<cap1>.)+',
         {'cap1': 'cap1_val'},
         ReverseParseError),

        # A non-capturing group with literals
        (r'(?:abc)',
         {},
         u'abc'),

        # A named capture nested within a non-capturing group, with literals
        (r'123(?:abc(?P<cap1>.)efg)456',
         {'cap1': 'cap1_val'},
         r'123abccap1_valefg456'),
        
        # max repetitions
        (r'(?P<cap1>a{16})', 
         {'cap1': 'cap1_val'}, 
         r'cap1_val'),

    ]

    def test_special_sequences(self):
        for re_str, kwargs, expected in self.special_sequences:
            # print re_str, kwargs
            try:
                out = reverse(re_str, kwargs)
                self.assertEqual(out, expected)
            except Exception as e:
                self.assertEqual(type(e), expected)

    def test_capture_groups(self):
        for re_str, kwargs, expected in self.capture_groups:
            # print re_str, kwargs
            try:
                out = reverse(re_str, kwargs)
                self.assertEqual(out, expected)
            except Exception as e:
                print re_str, out
                self.assertEqual(type(e), expected)


if __name__ == '__main__':
    unittest.main()
