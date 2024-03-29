"""Custom Jinja2 extensions for SQHG's backend."""

import os

from jinja2 import nodes
from jinja2.ext import Extension
from markupsafe import Markup


class StaticFilesExtension(Extension):
    tags = {'static'}

    def __init__(self, environment) -> None:
        super().__init__(environment)
        self.static_url = '/static/'
        self.static_dirs = environment.static_dirs

    def parse(self, parser) -> nodes.CallBlock:
        token = next(parser.stream)
        args = [parser.parse_expression()]

        return nodes.CallBlock(self.call_method('_render_static', args), [], [], []).set_lineno(token.lineno)

    def _render_static(self, url, caller) -> Markup:  # noqa: ARG002
        for static_dir in self.static_dirs:
            path = os.path.join(static_dir, url.lstrip('/'))
            if os.path.isfile(path):
                return Markup(self.static_url + url)
        raise ValueError(f'File not found: {url}')
