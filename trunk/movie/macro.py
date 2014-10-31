# -*- coding: utf-8 -*-
"""
    Movie plugin for Trac.

    Embeds various online movies.
"""

from urlparse import urlparse, urlunparse

from genshi.builder import tag
from trac.core import TracError
from trac.core import implements
from trac.resource import Resource, get_resource_url
from trac.web.chrome import ITemplateProvider, add_script
from trac.wiki.api import parse_args
from trac.wiki.macros import WikiMacroBase

from model import MovieMacroConfig
from utils import string_keys, xform_style, xform_query


EMBED_COUNT = '_moviemacro_embed_count'
FLOWPLAYER_EMBEDDED = '_moviemacro_flowplayer_embedded'


class MovieMacro(WikiMacroBase):
    """ Embed online movies from YouTube, GoogleVideo and MetaCafe, and local
        movies via FlowPlayer.
    """

    implements(ITemplateProvider)

    # IWikiMacroProvider methods
    def expand_macro(self, formatter, name, content):
        args, kwargs = parse_args(content, strict=True)
        kwargs = string_keys(kwargs)

        if len(args) >= 1:
            url = args[0]
        elif len(args) == 0:
            raise TracError('URL to a movie at least required.')

        embed_count = getattr(formatter, EMBED_COUNT, 0)
        embed_count += 1
        setattr(formatter, EMBED_COUNT, embed_count)

        url = self._get_absolute_url(formatter.req, url)
        scheme, netloc, path, params, query, fragment = urlparse(url)

        try:
            style_dict = xform_style(kwargs.get('style', ''))
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

        if netloc in ('www.youtube.com', 'www.youtube-nocookie.com'):
            return self.embed_youtube(scheme, netloc, path, params, query, style)

        if netloc == 'www.metacafe.com':
            return self.embed_metacafe(scheme, netloc, path, params, query, style)

        if netloc in ('vimeo.com', 'www.vimeo.com'):
            return self.embed_vimeo(scheme, netloc, path, params, query, style)

        # Local movies.
        return self.embed_player(url, kwargs, style, formatter)

    def embed_youtube(self, scheme, netloc, path, params, query, style):
        query_dict = xform_query(query)
        video = query_dict.get('v')
        url = urlunparse((scheme, netloc, '/v/%s' % video, '', '', ''))
        return tag.object(tag.param(name='movie', value=url),
                          tag.param(name='allowFullScreen', value='true'),
                          tag.embed(
                              src=url,
                              type='application/x-shockwave-flash',
                              allowfullscreen='true',
                              width=style['width'],
                              height=style['height']),
                          style=xform_style(style))

    def embed_metacafe(self, scheme, netloc, path, params, query, style):
        parts = path.split('/')
        try:
            path = '/fplayer/%s/%s.swf' % (parts[2], parts[3])
        except:
            raise TracError("Non-standard URL, don't know how to process it, file a ticket please.")
        url = urlunparse((scheme, netloc, path, '', '', ''))
        return tag.embed(src=url,
                         wmode='transparent',
                         pluginspage='http://www.macromedia.com/go/getflashplayer',
                         type='application/x-shockwave-flash',
                         style=xform_style(style))

    def embed_vimeo(self, scheme, netloc, path, params, query, style):
        parts = filter(None, path.split('/'))
        path = '/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1' % parts[0]
        url = urlunparse((scheme, netloc, path, '', '', ''))
        return tag.object(tag.param(name='movie', value=url),
                          tag.param(name='allowfullscreen', value='true'),
                          tag.param(name='allowscriptaccess', value='always'),
                          tag.embed(
                              src=url,
                              type='application/x-shockwave-flash',
                              allowfullscreen='true',
                              allowscriptaccess='always',
                              width=style['width'],
                              height=style['height']),
                          style=xform_style(style))

    def embed_player(self, url, kwargs, style, formatter):
        tags = []
        if not getattr(formatter, FLOWPLAYER_EMBEDDED, False):
            add_script(formatter.req, 'movie/js/flashembed.min.js')
            add_script(formatter.req, 'movie/js/flow.embed.js')
            script = '''
                $(function() {
                    $("a.flowplayer").flowembed("%s",  {initialScale:'scale'});
                });
            ''' % self._get_absolute_url(formatter.req, 'htdocs://movie/swf/FlowPlayerDark.swf')
            tags.append(tag.script(script))
            setattr(formatter, FLOWPLAYER_EMBEDDED, True)

        if kwargs.pop('clear', None) == 'none':
            style.pop('clear')

        kwargs = {'style': xform_style(style)}
        src = self._get_absolute_url(formatter.req, kwargs.pop('splash', 'htdocs://movie/img/black.jpg'))
        tags.append(tag.a(tag.img(src=src, **kwargs), class_='flowplayer', href=url, **kwargs))
        return ''.join([str(i) for i in tags])

    # ITemplateProvider methods

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [('movie', resource_filename('movie', 'htdocs'))]

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
            return get_resource_url(self.env, resource, req.abs_href, format='raw')

        return url
