import unittest

from surly.re_parse import reverse_template_js

class JSTestCase(unittest.TestCase):
    def test_js_simple(self):
        value = reverse_template_js(r'a')
        assert value == 'function(fields){return ""+"a";}', value
    def test_quotes(self):
        value = reverse_template_js(r'\'"')
        expected = '''function(fields){return ""+"'"+'"';}'''
        print '>', expected, '<'
        print '>', value, '<'
        assert value == expected, value
    def test_values(self):
        value = reverse_template_js(r'(?P<foo>\d+)aa')
        expected = '''function(fields){return ""+fields["foo"]+"a"+"a";}'''
        print '>', expected, '<'
        print '>', value, '<'
        assert value == expected, value