"""Custom Jinja2 extensions for SQHG's backend."""

import os

from jinja2 import nodes
from jinja2.ext import Extension


class StaticFilesExtension(Extension):
    tags = {'static'}

    def __init__(self, environment):
        super().__init__(environment)
        self.static_url = '/static/'
        self.static_root = environment.static_dirs

    def parse(self, parser):
        token = next(parser.stream)
        args = [nodes.Const(self.static_url + token.value)]
        return nodes.CallBlock(self.call_method('_render_static', args), [], [], []).set_lineno(token.lineno)

    def _render_static(self, url, caller):
        for static_dir in self.static_dirs:
            path = os.path.join(static_dir, url.lstrip('/'))
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    contents = f.read()
                return contents
        raise ValueError('File not found: {}'.format(url))
