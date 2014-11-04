# -*- coding: utf-8 -*-
import re
import urllib

from trac.core import Component, implements
from trac.mimeview.api import IHTMLPreviewRenderer
from trac.wiki.formatter import format_to_html


PREVIEW_PATH = r'/.*?/raw-attachment/(?P<realm>.*?)/(?P<path>.*)$'


class MoviePreviewRenderer(Component):

    implements(IHTMLPreviewRenderer)

    ENCODING = 'utf-8'
    MACRO_FORMAT = '[[Movie(%(realm)s://%(path)s)]]'
    MIMETYPE_PREFIX = 'video/'
    PREVIEW_PATTERN = re.compile(PREVIEW_PATH)

    # IHTMLPreviewRenderer methods

    def get_quality_ratio(self, mimetype):
        if mimetype.startswith(self.MIMETYPE_PREFIX):
            return 9
        return 0

    def render(self, context, mimetype, content, filename=None, url=None):
        if url is not None:
            match = re.match(self.PREVIEW_PATTERN, urllib.unquote(str(url)))
            if match:
                path_info = match.groupdict()
                macro = unicode(self.MACRO_FORMAT % path_info, self.ENCODING)
                return format_to_html(self.env, context, macro)
        return None
