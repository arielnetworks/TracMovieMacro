# -*- coding: utf-8 -*-
from os.path import join as pathjoin


def string_keys(d):
    """ Convert unicode keys into string keys, suiable for func(**d) use.
    >>> {} == string_keys({})
    True
    >>> {'x': 1, 'y': 2} == string_keys({u'x': 1, u'y': 2})
    True
    """
    return dict((str(key), value) for key, value in d.items())


def _xform_to_dict(style, first_sep, second_sep):
    """
    >>> d = {'display': 'none', 'clear': 'both'}
    >>> d == _xform_to_dict('display: none; clear: both;', ';', ':')
    True
    """
    return dict((s.strip() for s in i.split(second_sep, 1))
                for i in filter(None, style.split(first_sep)))


def xform_style(style):
    """ Convert between a style-string and a style-dictionary.
    >>> xform_style({})
    ''
    >>> xform_style('')
    {}
    >>> xform_style({'display': 'none'})
    'display: none;'
    >>> xform_style('clear: both;')
    {'clear': 'both'}
    >>> style = {'width': u'320px', 'height': u'240px', 'display': 'none'}
    >>> style == xform_style(xform_style(style))
    True
    """
    if isinstance(style, dict):
        result = '; '.join(['%s: %s' % (k, v) for k, v in style.items()])
        if result:
            result += ';'
        return result
    else:
        return _xform_to_dict(style, ';', ':')


def xform_query(query):
    """ Convert between a query-string and a query-dictionary.
    >>> xform_query({})
    ''
    >>> xform_query('')
    {}
    >>> xform_query({u'v': u'9dfWzp7rYR4'})
    u'v=9dfWzp7rYR4'
    >>> xform_query('v=9dfWzp7rYR4')
    {'v': '9dfWzp7rYR4'}
    >>> query = {'t': '1414735598', 'key': 'bW92aWVtYWNybw=='}
    >>> query == xform_query(xform_query(query))
    True
    """
    if isinstance(query, dict):
        return '&'.join(['%s=%s' % (k, v) for k, v in query.items()])
    else:
        return _xform_to_dict(query, '&', '=')


def set_default_parameters(param, default, **kwargs):
    """
    >>> param = {'width': '320', 'test': '1'}
    >>> default = {'width': '640', 'height': '360', 'test': '0', 'p': None}
    >>> set_default_parameters(param, default, test='2')
    >>> sorted(param.items())
    [('height', '360'), ('test', '2'), ('width', '320')]
    """
    for key, value in default.items():
        if param.get(key) is None:
            if value is not None:
                param[key] = value
    if kwargs:
        for key, value in kwargs.items():
            param[key] = value


def parse_imagemacro_style(url, path_info):
    """
    >>> parse_imagemacro_style(u'file.ext', u'/ticket/1')
    (u'ticket', u'1', u'file.ext')
    >>> parse_imagemacro_style(u'ticket:1:file.ext', u'/ticket/1')
    (u'ticket', u'1', u'file.ext')
    >>> parse_imagemacro_style(u'ticket:2:file.ext', u'/ticket/1')
    (u'ticket', u'2', u'file.ext')
    >>> parse_imagemacro_style(u'file.ext', u'/wiki/start')
    (u'wiki', u'start', u'file.ext')
    >>> parse_imagemacro_style(u'file.ext', u'/wiki/start/sub/deep')
    (u'wiki', u'start', u'sub/deep/file.ext')
    >>> url = u'wiki:start/sub/deep/file.ext'
    >>> parse_imagemacro_style(url, u'/wiki/start/sub/deep')
    (u'wiki', u'start', u'sub/deep/file.ext')
    >>> parse_imagemacro_style(u'wiki:start/file.ext', u'/wiki/start')
    (u'wiki', u'start', u'file.ext')
    """
    _path, netloc = '', ''
    _path_info = filter(None, path_info.split('/'))
    scheme = _path_info[0]
    if len(_path_info) > 1:
        netloc = _path_info[1]
        _path = '/'.join(_path_info[2:])

    _url = url.split(':')
    if scheme == 'ticket' and len(_url) == 3:
        netloc = _url[1]

    path = _url[-1]
    if scheme != 'ticket':
        if len(_url) == 1:
            path = pathjoin(_path, path)
        else:
            path = path.split('/', 1)[-1]

    return scheme, netloc, path
