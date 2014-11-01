# -*- coding: utf-8 -*-
from os.path import join as pathjoin


class MovieMacroConfig(object):
    """Configuration model to handle MovieMacro settings."""

    SECTION = 'moviemacro'
    DEFAULT_WIDTH = '640'
    DEFAULT_HEIGHT = '360'
    DEFAULT_SPLASH = None

    def __init__(self, env, config):
        self.env = env
        self.config = config

    @property
    def width(self):
        return self.config.get(self.SECTION, 'width', self.DEFAULT_WIDTH)

    @property
    def height(self):
        return self.config.get(self.SECTION, 'height', self.DEFAULT_HEIGHT)

    @property
    def splash(self):
        splash = self.config.get(self.SECTION, 'splash', self.DEFAULT_SPLASH)
        if splash:
            splash = pathjoin('movie/img', splash)
        return splash
