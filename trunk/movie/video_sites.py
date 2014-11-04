# -*- coding: utf-8 -*-
"""
    Support Video Sharing Sites

    Define embed player tag and set VIDEO_SHARING_SITES
    to resolve site name and player function
"""
import mimetypes
from urllib import urlencode
from urlparse import urlunparse

from genshi.builder import tag
from trac.core import TracError

from utils import set_default_parameters, xform_style, xform_query

SWF_MIME_TYPE = mimetypes.types_map.get('.swf')


def get_embed_video_site_player(netloc):
    for sites, func in VIDEO_SHARING_SITES.items():
        if netloc in sites:
            return func
    return None


_EMBED_YOUTUBE_DEFAULT_PARAMETERS = {
    'autohide': '2',
    'autoplay': '0',
    'cc_load_policy': None,
    'color': 'red',
    'controls': '1',
    'disablekb': '0',
    'enablejsapi': '0',
    'end': None,
    'fs': '1',
    'hl': None,
    'iv_load_policy': '1',
    'list': None,
    'listType': None,
    'loop': '0',
    'modestbranding': '1',
    'origin': None,
    'playerapiid': None,
    'playlist': None,
    'playsinline': None,
    'rel': '0',
    'showinfo': '0',
    'start': None,
    'theme': 'dark',
}


def embed_youtube(scheme, netloc, path, query, style):
    """
    Embed youtube player using iframe.
    _EMBED_YOUTUBE_DEFAULT_PARAMETERS is set to the embed player.

    see also: https://developers.google.com/youtube/player_parameters
    """
    query_dict = xform_query(query)
    set_default_parameters(query_dict, _EMBED_YOUTUBE_DEFAULT_PARAMETERS)
    video_id = query_dict.pop('v')
    query = urlencode(query_dict.items())
    url = urlunparse((scheme, netloc, '/embed/%s' % video_id, '', query, ''))
    return tag.iframe(src=url, style=xform_style(style))


def embed_metacafe(scheme, netloc, path, query, style):
    parts = filter(None, path.split('/'))
    try:
        path = '/embed/%s/' % parts[1]
    except:
        msg = "Non-standard URL, "\
              "don't know how to process it, file a ticket please."
        raise TracError(msg)
    return tag.iframe(
        src=urlunparse((scheme, netloc, path, '', '', '')),
        allowFullScreen='true',
        frameborder=0,
        width=style['width'],
        height=style['height'],
        style=xform_style(style)
    )


def embed_vimeo(scheme, netloc, path, query, style):
    parts = filter(None, path.split('/'))
    path = '/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;'\
           'show_title=1&amp;show_byline=1&amp;'\
           'show_portrait=0&amp;color=&amp;fullscreen=1' % parts[0]
    url = urlunparse((scheme, netloc, path, '', '', ''))
    return tag.object(
        tag.param(name='movie', value=url),
        tag.param(name='allowfullscreen', value='true'),
        tag.param(name='allowscriptaccess', value='always'),
        tag.embed(
            src=url,
            type=SWF_MIME_TYPE,
            allowfullscreen='true',
            allowscriptaccess='always',
            width=style['width'],
            height=style['height']
        ),
        style=xform_style(style)
    )


VIDEO_SHARING_SITES = {
    ('www.youtube.com', 'www.youtube-nocookie.com'): embed_youtube,
    ('www.metacafe.com',): embed_metacafe,
    ('vimeo.com', 'www.vimeo.com'): embed_vimeo,
}
