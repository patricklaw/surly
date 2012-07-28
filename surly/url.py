import re
from surly import re_parse

class URL(object):

    def __init__(self, re_str, name=None):
        self.re_str = re_str
        self.name = name
        self.regex = re.compile(self.re_str)
        self.reverse_template = re_parse.reverse_template(re_str)

    def match(self, url):
        return self.regex.match(url)

    def reverse(self, **kwargs):
        return self.reverse_template.format(**kwargs)

    