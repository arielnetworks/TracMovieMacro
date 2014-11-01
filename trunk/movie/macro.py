# -*- coding: utf-8 -*-
"""
    Movie plugin for Trac.

    Embeds various online movies.
"""
import mimetypes
from os.path import join as pathjoin
from urlparse import urlparse

from genshi.builder import tag
from pkg_resources import resource_filename
from trac.core import TracError
from trac.core import implements
from trac.resource import Resource, get_resource_url
from trac.web.chrome import ITemplateProvider, add_script, add_stylesheet
from trac.wiki.api import parse_args
from trac.wiki.macros import WikiMacroBase

from model import MovieMacroConfig
from utils import string_keys, xform_style
from video_sites import get_embed_video_site_player


EMBED_PATH_FLOWPLAYER = {
    'js': 'movie/js/flowplayer.min.js',
    'css': 'movie/js/skin/minimalist.css',
    'swf': 'movie/swf/flowplayer.swf',
}


class MovieMacro(WikiMacroBase):
    """ Embed online movies from YouTube, GoogleVideo and MetaCafe, and local
        movies via FlowPlayer.
    """
    implements(ITemplateProvider)

    # IWikiMacroProvider methods
    def expand_macro(self, formatter, name, content):
        args, kwargs = parse_args(content, strict=True)
        if len(args) == 0:
            raise TracError('URL to a movie at least required.')

        url = self._get_absolute_url(formatter.req, args[0])
        scheme, netloc, path, params, query, fragment = urlparse(url)

        try:
            style_dict = xform_style(string_keys(kwargs).get('style', ''))
        except:
            raise TracError('Double check the `style` argument.')

        config = MovieMacroConfig(self.env, self.config)
        style = {
            'width': style_dict.get('width', config.width),
            'height': style_dict.get('width', config.height),
            'border': style_dict.get('border', 'none'),
            'margin': style_dict.get('margin', '0 auto'),
            'display': 'block',
            'clear': 'both'
        }

        site_player = get_embed_video_site_player(netloc)
        if site_player is not None:
            return site_player(scheme, netloc, path, query, style)

        if config.splash:
            splash_url = pathjoin(formatter.href.chrome(), config.splash)
            splash_style = 'background-color:#777; '\
                           'background-image:url(%s);' % splash_url
            style['style'] = splash_style
        return self.embed_player(formatter, url, style)

    def embed_player(self, formatter, url, style):
        add_script(formatter.req, EMBED_PATH_FLOWPLAYER['js'])
        add_stylesheet(formatter.req, EMBED_PATH_FLOWPLAYER['css'])
        swf = pathjoin(formatter.href.chrome(), EMBED_PATH_FLOWPLAYER['swf'])
        attrs = {
            'data-swf': swf,
            'data-ratio': '0.4167',
            'style': xform_style(style),
        }
        return tag.div(
            tag.video(
                tag.source(type=mimetypes.guess_type(url)[0], src=url),
            ),
            class_='flowplayer',
            **attrs)

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        yield ('movie', resource_filename('movie', 'htdocs'))

    def get_templates_dirs(self):
        return []

    # Private methods

    def _get_absolute_url(self, req, url):
        """ Generate an absolute url from the url with the special schemes
        {htdocs,chrome,ticket,wiki,source} simply return the url if given with
        {http,https,ftp} schemes.

        Examples:
            http://example.com/filename.ext
                ie. http://www.google.com/logo.jpg

            chrome://site/filename.ext
            htdocs://img/filename.ext
                note: `chrome` is an alias for `htdocs`

            ticket://number/attachment.pdf
                ie. ticket://123/specification.pdf

            wiki://WikiWord/attachment.jpg

            source://changeset/path/filename.ext
                ie. source://1024/trunk/docs/README
        """
        scheme, netloc, path, query, params, fragment = urlparse(url)

        if scheme in ('htdocs', 'chrome'):
            return req.abs_href.chrome(netloc + path)

        if scheme in ('source',):
            return req.abs_href.export(netloc + path)

        if scheme in ('wiki', 'ticket'):
            resource = Resource(scheme, netloc).child('attachment', path)
            kwargs = {'format': 'raw'}
            return get_resource_url(self.env, resource, req.abs_href, **kwargs)

        return url
