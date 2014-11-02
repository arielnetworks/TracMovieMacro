# -*- coding: utf-8 -*-
import pytest

from movie.utils import _xform_to_dict
from movie.utils import parse_imagemacro_style
from movie.utils import set_default_parameters
from movie.utils import string_keys
from movie.utils import xform_query
from movie.utils import xform_style


@pytest.mark.parametrize(('d', 'expected'), [
    ({}, {}),
    ({u'x': 1, u'y': 2}, {'x': 1, 'y': 2}),
])
def test_string_keys(d, expected):
    assert expected == string_keys(d)


@pytest.mark.parametrize(('style', 'first_sep', 'second_sep', 'expected'), [
    ('display: none; clear: both;', ';', ':',
     {'display': 'none', 'clear': 'both'}),
])
def test_xform_to_dict(style, first_sep, second_sep, expected):
    assert expected == _xform_to_dict(style, first_sep, second_sep)


@pytest.mark.parametrize(('style', 'expected'), [
    ({}, ''),
    ('', {}),
    ({'display': 'none'}, 'display: none;'),
    ('clear: both;', {'clear': 'both'}),
])
def test_xform_style_simple(style, expected):
    assert expected == xform_style(style)


@pytest.mark.parametrize('style', [
    {'width': u'320px', 'height': u'240px', 'display': 'none'},
])
def test_xform_style_multi(style):
    assert style == xform_style(xform_style(style))


@pytest.mark.parametrize(('query', 'expected'), [
    ({}, ''),
    ('', {}),
    ({u'v': u'9dfWzp7rYR4'}, u'v=9dfWzp7rYR4'),
    ('v=9dfWzp7rYR4', {'v': '9dfWzp7rYR4'}),
])
def test_xform_query_simple(query, expected):
    assert expected == xform_query(query)


@pytest.mark.parametrize('query', [
    {'t': '1414735598', 'key': 'bW92aWVtYWNybw=='}
])
def test_xform_query_multi(query):
    assert query == xform_query(xform_query(query))


@pytest.mark.parametrize(('param', 'default', 'kwargs', 'expected'), [
    (
        {'width': '320', 'test': '1'},
        {'width': '640', 'height': '360', 'test': '0', 'p': None},
        {'test': '2'},
        {'width': '320', 'height': '360', 'test': '2'}
    ),
])
def test_set_default_parameters(param, default, kwargs, expected):
    set_default_parameters(param, default, **kwargs)
    assert expected == param


@pytest.mark.parametrize(('url', 'path_info', 'expected'), [
    ('file.ext', '/ticket/1', ('ticket', '1', 'file.ext')),
    ('ticket:1:file.ext', '/ticket/1', ('ticket', '1', 'file.ext')),
    ('ticket:2:file.ext', '/ticket/1', ('ticket', '2', 'file.ext')),
    ('file.ext', '/wiki/start', ('wiki', 'start', 'file.ext')),
    ('file.ext', '/wiki/start/sub/deep',
        ('wiki', 'start', 'sub/deep/file.ext')),
    ('wiki:start/sub/deep/file.ext', '/wiki/start/sub/deep',
        ('wiki', 'start', 'sub/deep/file.ext')),
    ('wiki:start/file.ext', '/wiki/start', ('wiki', 'start', 'file.ext')),
])
def test_parse_imagemacro_style(url, path_info, expected):
    assert expected == parse_imagemacro_style(url, path_info)
