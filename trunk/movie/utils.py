# -*- coding: utf-8 -*-


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
