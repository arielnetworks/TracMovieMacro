# -*- coding: utf-8 -*-


class MovieMacroConfig(object):
    """Configuration model to handle MovieMacro settings."""

    SECTION = 'moviemacro'
    DEFAULT_WIDTH = '640px'
    DEFAULT_HEIGHT = '360px'

    def __init__(self, env, config):
        self.env = env
        self.config = config

    @property
    def width(self):
        return self.config.get(self.SECTION, 'width', self.DEFAULT_WIDTH)

    @property
    def height(self):
        return self.config.get(self.SECTION, 'height', self.DEFAULT_HEIGHT)
