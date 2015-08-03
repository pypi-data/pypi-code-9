# -*- coding: utf-8 -*-
import sys
import os
from core.transition import render_template_string
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import mediatumbabel
import mediatumbabel as babel
from mediatumbabel import gettext, ngettext, lazy_gettext

from fixtures import app_german, b


def test_locale_setting(app_german, b):
    with app_german.test_request_context():
        assert mediatumbabel.get_locale() == babel.Locale.parse("de")


def test_basics(app_german, b):
    """
    :type app: AthanaFlaskStyleApp
    :type b: Babel
    """
    with app_german.test_request_context():
        assert gettext(u'Hello %(name)s!', name='Peter') == 'Hallo Peter!'
        assert ngettext(u'%(num)s Apple', u'%(num)s Apples', 3) == u'3 Äpfel'
        assert ngettext(u'%(num)s Apple', u'%(num)s Apples', 1) == u'1 Apfel'


def test_template_basics(app_german, b):
    t = lambda x: render_template_string('{{ %s }}' % x)

    with app_german.test_request_context():
        assert t("gettext('Hello %(name)s!', name='Peter')") == 'Hallo Peter!'
        assert t("ngettext('%(num)s Apple', '%(num)s Apples', 3)") == u'3 Äpfel'
        assert t("ngettext('%(num)s Apple', '%(num)s Apples', 1)") == u'1 Apfel'
        assert render_template_string('''
            {% trans %}Hello {{ name }}!{% endtrans %}
        ''', name='Peter').strip() == 'Hallo Peter!'
        assert render_template_string('''
            {% trans num=3 %}{{ num }} Apple
            {%- pluralize %}{{ num }} Apples{% endtrans %}
        ''', name='Peter').strip() == u'3 Äpfel'


def test_lazy_gettext(app_german, b):
    yes = lazy_gettext(u'Yes')
    with app_german.test_request_context():
        assert yes == 'Ja'
    app_german.config['BABEL_DEFAULT_LOCALE'] = 'en_US'
    with app_german.test_request_context():
        assert yes == 'Yes'


def test_list_translations(app_german, b):
    translations = b.list_translations()
    assert len(translations) == 1
    assert str(translations[0]) == 'de'


def test_list_translations_with_multiple_translations_dirs(app_german, b):
    b.add_translations_dir("translations2")
    translations = b.list_translations()
    assert len(translations) == 2
    assert str(translations[1]) == 'de_AT'


def test_gettext_with_multiple_translations_dirs(app_german, b):
    b.add_translations_dir("translations2")
    with app_german.test_request_context():
        app_german.config['BABEL_DEFAULT_LOCALE'] = 'de_AT'
        assert gettext(u'Hello %(name)s!', name='Peter') == 'Hallo Peter!'