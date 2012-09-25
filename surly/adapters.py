import re

class SurlyTornadoMixin(object):
    def reverse(self, name, **kwargs):
        """Returns a URL path for handler named `name`

        The handler must be added to the application as a 
        surly pattern.

        Keyword args will be substituted for capturing groups in the 
        URLSpec regex. They will be converted to strings if necessary, 
        encoded as utf8, and url-escaped.
        """
        if name in self.application.named_handlers:
            return self.application.named_handlers[name].reverse(**kwargs)
        raise KeyError("%s not found in named urls" % name)

class TornadoUrlSpec(object):
    def __init__(self, url):
        self.url = url
        self.regex = re.compile(self.url.pattern)
    @property
    def kwargs(self):
        return self.url.extra_args or {}
    @property
    def handler_class(self):
        return self.url.target
    @property
    def name(self):
        return self.url.name

    def reverse(self, **kwargs):
        return self.url.reverse(**kwargs)

def wrap_tornado(mapper):
    ''' Turn the surly url objects objects which works
        with Tornado
    '''
    return [TornadoUrlSpec(url) for url in mapper.urls]

