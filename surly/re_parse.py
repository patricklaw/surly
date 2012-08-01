import sre_parse
import re


class ReverseParseError(Exception):
    pass

class PythonReverser(object):
    ''' Python format string reverser.  Generates a python format
        string which will produce a URL.'''

    def __init__(self):
        self.s = ''
    def add_literal(self, char):
        ''' Append a literal character to the format string
        '''
        self.s += char
    def add_named_group(self, name):
        ''' Add a variable to the format string group to the JS expression 
            (e.g. {name})

            :param name: the name of the capture group
            :type name: string
        '''
        self.s += '{%s}' % name
    def value(self):
        return self.s

class JavascriptReverser(object):
    ''' Super-quick javascript reverser.  Generates an anonymous function 
        which can take an object as a parameter and produce a URL.  Since URLs
        are not user generated, there is no effort to stop cross-site scripting
    '''
    def __init__(self):
        self.s = ''
    def add_literal(self, char):
        ''' Append a literal character to the JS expression.  The function 
            handles single and double quotes.
        '''
        if char == '"':
            self.s += "+'%s'" % char
        else:
            self.s += '+"%s"' % char
    def add_named_group(self, name):
        ''' Add a named group to the JS expression, having it append
            fields["name"]

            :param name: the name of the capture group
            :type name: string
        '''
        self.s += '+fields["%s"]' % name
    def value(self):
        ''' Returns the anonymous JS function built up over the course of 
            parsing

            :rtype: string
        '''
        return '''function(fields){return ""%s;}''' % self.s

def _recursive_parse(ast, group_index_map, *reversers):
    '''
    This relies heavily on the implementation of the standard 
    library module sre_parse, particularly the functions parse and _parse.

    Regular expressions with named capture groups are supported.
    Non-capturing groups are also supported; their contents are recursively
    parsed.

    Any non-literal expressions occurring outside of a named capture group
    are not supported.

    No attempt is made to make this code fast or safe.
    '''
    for item in ast:
        item_type = item[0]
        if item_type == 'literal':
            # This is a matched literal; keep it
            for r in reversers:
                r.add_literal(unichr(item[1]))
        elif item_type == 'subpattern':
            subpattern = item[1]
            subpattern_index = subpattern[0]

            if subpattern_index is None:
                # This is a non-capturing group.  Parse it out recursively.
                _recursive_parse(subpattern[1], group_index_map, *reversers)
            else:
                # Otherwise, we've found a capture group.  Fill in our value.
                # s += kwargs[group_index_map[subpattern_index]]
                for r in reversers:
                    r.add_named_group(group_index_map[subpattern_index])
        elif item_type == 'at' and item[1] == 'at_end':
            pass
        elif item_type == 'at' and item[1] == 'at_beginning':
            pass
        # elif item_type == 'max_repeat':
        #     pass
        # elif item_type == 'any':
        #     pass
        else:
            raise ReverseParseError('Unsupported regex expression: %s'
                                    % item_type)

def reverse_template(re_str):
    ''' Turn a regular expression into a python format string

        :param re_str: the regular expression
        :type re_str: string
    '''
    reverser = PythonReverser()
    _reverse_template(re_str, reverser)
    return reverser.value()

def reverse_template_js(re_str):
    ''' Turn a regular expression into an anonymous JS function which
        can be used to generate URLs

        :param re_str: the regular expression
        :type re_str: string
    '''
    reverser = JavascriptReverser()
    _reverse_template(re_str, reverser)
    return reverser.value()

def _reverse_template(re_str, reverser):
    '''
    `reverse_template` generates a python string formatting template \
    based on the capture groups in the regex ``re_str``.

    :param re_str: A Python string (raw strings are recommended) \
    representing the regular expression to be reversed.
    '''

    r = re.compile(re_str)
    ast = sre_parse.parse(re_str)
    group_indices = r.groupindex
    group_index_map = dict((index, group) 
                           for (group, index) in r.groupindex.items())

    _recursive_parse(ast, group_index_map, reverser)


def reverse(re_str, kwargs):
    '''
    `reverse` interpolates `kwargs` values into their respective named \
    capture groups within `re_str`.

    :param re_str: A Python string (raw strings are recommended) \
    representing the regular expression to be reversed.
    :param kwargs: A dictionary mapping capture group names to the \
    value that should be interpolated into the capture expression.
    '''

    r = re.compile(re_str)
    ast = sre_parse.parse(re_str)
    group_indices = r.groupindex
    group_index_map = dict((index, group) 
                           for (group, index) in r.groupindex.items())
    python_reverser = PythonReverser()
    _recursive_parse(ast, group_index_map, python_reverser)
    s = python_reverser.value().format(**kwargs)
    return s

def reverse_group_map(re_str):
    r = re.compile(re_str)
    ast = sre_parse.parse(re_str)
    group_indices = r.groupindex
    group_index_map = dict((index, group) 
                           for (group, index) in r.groupindex.items())
    return group_index_map
