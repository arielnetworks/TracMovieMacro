# -*- coding: utf-8 -*-
import pytest

from movie.video_sites import VIDEO_SHARING_SITES
from movie.video_sites import get_embed_video_site_player


def test_exist_embed_function():
    for sites, func in VIDEO_SHARING_SITES.items():
        assert callable(func)


@pytest.mark.parametrize(('netloc', 'expected'), [
    ('unknown.com', None),
    ('www.youtube.com', 'embed_youtube'),
    ('www.youtube-nocookie.com', 'embed_youtube'),
    ('www.metacafe.com', 'embed_metacafe'),
    ('vimeo.com', 'embed_vimeo'),
    ('www.vimeo.com', 'embed_vimeo'),
])
def test_get_embed_video_site_player(netloc, expected):
    player = get_embed_video_site_player(netloc)
    if player is None:
        assert player is expected
    else:
        assert expected == player.func_name
