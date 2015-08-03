# -*- coding: utf-8 -*-
"""
Copyright (C) 2013 Tobias Stenzel <tobias.stenzel@tum.de>
"""

from pytest import fixture
from mediatumbabel import Babel
from core.transition import create_app

current_app = None


@fixture
def app():
    global current_app
    current_app = create_app(__name__)
    Babel(current_app, translations_dirs=["translations"])
    return current_app


@fixture
def app_german():
    global current_app
    current_app = create_app(__name__)
    Babel(current_app, default_locale="de", translations_dirs=["translations"])
    return current_app


@fixture
def b():
    return current_app.extensions["babel"]


