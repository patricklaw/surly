import sre_parse
import re


class ReverseParseError(Exception):
    pass

def _recursive_parse(ast, group_index_map):
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

    s = ''

    for item in ast:
        item_type = item[0]
        if item_type == 'literal':
            # This is a matched literal; keep it
            s += unichr(item[1])
        elif item_type == 'subpattern':
            subpattern = item[1]
            subpattern_index = subpattern[0]

            if subpattern_index is None:
                # This is a non-capturing group.  Parse it out recursively.
                s += _recursive_parse(subpattern[1], group_index_map)
            else:
                # Otherwise, we've found a capture group.  Fill in our value.
                # s += kwargs[group_index_map[subpattern_index]]
                s += '{%s}' % group_index_map[subpattern_index]
        elif item_type == 'at' and item[1] == 'at_end':
            pass
        elif item_type == 'at' and item[1] == 'at_beginning':
            pass
        else:
            raise ReverseParseError('Unsupported regex expression: %s'
                                    % item_type)

    return s


def reverse_template(re_str):
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

    t = _recursive_parse(ast, group_index_map)
    return t

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

    t = _recursive_parse(ast, group_index_map)
    s = t.format(**kwargs)
    return s

