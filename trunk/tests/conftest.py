# -*- coding: utf-8 -*-
from trac.attachment import AttachmentModule
from trac.resource import ResourceSystem
from trac.test import EnvironmentStub

from movie.macro import MovieMacro
from movie.web_ui import MoviePreviewRenderer


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption('--envscope',
                    action="store", dest="envscope", default="module",
                    type="choice", choices=["module", "function"],
                    help=("set environment scope, default: module."))


def make_trac_environment_with_plugin():
    env = EnvironmentStub(enable=["movie.*", MovieMacro, MoviePreviewRenderer])
    resource_system = ResourceSystem(env)
    resource_system._resource_managers_map = {
        'attachment': AttachmentModule(env),
    }
    movie_macro = MovieMacro(env)
    preview_renderer = MoviePreviewRenderer(env)
    return env, movie_macro, preview_renderer


def pytest_funcarg__env(request):
    setup = make_trac_environment_with_plugin
    scope = request.config.option.envscope
    env, _, _ = request.cached_setup(setup=setup, scope=scope)
    return env


def pytest_funcarg__movie_macro(request):
    setup = make_trac_environment_with_plugin
    scope = request.config.option.envscope
    _, movie_macro, _ = request.cached_setup(setup=setup, scope=scope)
    return movie_macro


def pytest_funcarg__preview_rendere(request):
    setup = make_trac_environment_with_plugin
    scope = request.config.option.envscope
    _, _, preview_renderer = request.cached_setup(setup=setup, scope=scope)
    return preview_renderer
