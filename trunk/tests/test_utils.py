# -*- coding: utf-8 -*-
import pytest

from movie.utils import string_keys
from movie.utils import _xform_to_dict
from movie.utils import xform_style
from movie.utils import xform_query


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
