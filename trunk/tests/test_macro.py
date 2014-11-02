# -*- coding: utf-8 -*-
import pytest

from trac.web.href import Href


BASE_HREF = 'http://example.com/mysite'


class Request(object):
    locale = None
    args = {}

    def __init__(self, **kwargs):
        self.chrome = {}
        for k, v in kwargs.items():
            setattr(self, k, v)


@pytest.mark.parametrize(('url', 'expected'), [
    ('http://example.com/file.ext', 'http://example.com/file.ext'),
    ('htdocs://site/test.flv', '%s/chrome/site/test.flv' % BASE_HREF),
    ('chrome://site/test.flv', '%s/chrome/site/test.flv' % BASE_HREF),
    ('ticket://123/sample.webm',
     '%s/raw-attachment/ticket/123/sample.webm' % BASE_HREF),
    ('wiki://page/sample.mp4',
     '%s/raw-attachment/wiki/page/sample.mp4' % BASE_HREF),
    ('source://repo/movie.ogv', '%s/export/repo/movie.ogv' % BASE_HREF),
])
def test_get_absolute_url(movie_macro, url, expected):
    req = Request(abs_href=Href(BASE_HREF))
    assert expected == movie_macro._get_absolute_url(req, url)


@pytest.mark.parametrize(('url', 'path_info', 'expected'), [
    ('sample.webm', u'/ticket/123',
     '%s/raw-attachment/ticket/123/sample.webm' % BASE_HREF),
    ('ticket:123:sample.webm', u'/ticket/123',
     '%s/raw-attachment/ticket/123/sample.webm' % BASE_HREF),
    ('wiki:sample.mp4', u'/wiki/page',
     '%s/raw-attachment/wiki/page/sample.mp4' % BASE_HREF),
    ('wiki:page/sample.mp4', u'/wiki/page',
     '%s/raw-attachment/wiki/page/sample.mp4' % BASE_HREF),
    ('wiki:test/movie/sub/sample.mp4', u'/wiki/test/movie/sub',
     '%s/raw-attachment/wiki/test/movie/sub/sample.mp4' % BASE_HREF),
])
def test_get_absolute_url_simple(movie_macro, url, path_info, expected):
    req = Request(abs_href=Href(BASE_HREF), path_info=path_info)
    assert expected == movie_macro._get_absolute_url(req, url)
