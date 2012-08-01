from surly.re_parse import reverse_template, reverse_template_js, reverse_group_map

class MapperError(Exception):
    pass

class Mapper(object):
    ''' The mapper is the framework-agnostic way of defining 
        URL mappings.  
    '''
    def __init__(self, urls, replacements={}):
        ''' :param urls: a list of ``url`` objects.  See ``url`` \
            for details
        '''
        self.urls = urls
        self.reverse_patterns = {}

        for u in urls:
            if replacements:
                u.apply_replacements(**replacements)
            if not u.name:
                continue
            if u.name in self.reverse_patterns:
                raise MapperError('Duplicate reversal name: %s' % u.name)
            self.reverse_patterns[u.name] = u
    def js_mapper(self, var_name):
        ''' Return a JS function which is the equivalent of the python 
            reverse mapper.  The reverse function is assigned to
            ``var_name``.  (e.g. if ``var_name`` is "Foo.Bar", the generated
            code will be "Foo.Bar = function(){...}")
        '''
        ret = '{var_name} = function(name, args){{'.format(var_name=var_name)
        ret += 'var mapping = {'
        for count, (name, u) in enumerate(self.reverse_patterns.items()):
            if count != 0:
                ret += ','
            function = u.js_pattern
            ret += '"{name}":{function}'.format(**vars())
        ret += '};' # end mapping
        ret += '''return mapping[name](args);'''
        ret += '};' # end function
        return ret

    def reverse(self, name, **kwargs):
        ''' return the URL for a name, interpolated with **kwargs '''
        if name not in self.reverse_patterns:
            raise MapperError('No reverse found for name: %s' % name)
        return self.reverse_patterns[name].reverse(**kwargs)

class url(object):
    ''' class for defining urls in the surly dsl.  Shouldn't be used 
        independently.
    '''
    def __init__(self, pattern, target, extra_args=None, name=None):
        ''' :param pattern: The URL pattern. Use named matching groups
            :type pattern: regular expression as a string
            :param target: An object which the url is mapped to.  
            :type target: Determined by the adapter being used.
        '''
        self.extra_args = extra_args
        self.name = name
        self.pattern = pattern
        self.target = target
        self.replacements_applied = False
        self._compile()

    def apply_replacements(self, **replacements):
        if self.replacements_applied:
            return
        self.pattern = self.pattern.format(**replacements)
        self._compile()
        self.replacements_applied = True

    def _compile(self):
        self.js_pattern = reverse_template_js(self.pattern)
        self.py_pattern = reverse_template(self.pattern)
        self.group_map = reverse_group_map(self.pattern)
    def reverse(self, **kwargs):
        ''' python-based reversal for this URL
        '''
        return self.py_pattern.format(**kwargs)


