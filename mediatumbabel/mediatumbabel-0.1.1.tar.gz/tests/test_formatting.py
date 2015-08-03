# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from decimal import Decimal
from datetime import datetime
import mediatumbabel as babel
from fixtures import app, b


def test_date_format_basics(app, b):
    d = datetime(2010, 4, 12, 13, 46)

    with app.test_request_context():
        assert babel.format_datetime(d) == 'Apr 12, 2010, 1:46:00 PM'
        assert babel.format_date(d) == 'Apr 12, 2010'
        assert babel.format_time(d) == '1:46:00 PM'

    with app.test_request_context():
        app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Vienna'
        assert babel.format_datetime(d) == 'Apr 12, 2010, 3:46:00 PM'
        assert babel.format_date(d) == 'Apr 12, 2010'
        assert babel.format_time(d) == '3:46:00 PM'

    with app.test_request_context():
        app.config['BABEL_DEFAULT_LOCALE'] = 'de_DE'
        assert babel.format_datetime(d, 'long') == \
            '12. April 2010 15:46:00 MESZ'


def test_init_app(app, b):
    b.init_app(app)
    d = datetime(2010, 4, 12, 13, 46)

    with app.test_request_context():
        assert babel.format_datetime(d) == 'Apr 12, 2010, 1:46:00 PM'
        assert babel.format_date(d) == 'Apr 12, 2010'
        assert babel.format_time(d) == '1:46:00 PM'

    with app.test_request_context():
        app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Vienna'
        assert babel.format_datetime(d) == 'Apr 12, 2010, 3:46:00 PM'
        assert babel.format_date(d) == 'Apr 12, 2010'
        assert babel.format_time(d) == '3:46:00 PM'

    with app.test_request_context():
        app.config['BABEL_DEFAULT_LOCALE'] = 'de_DE'
        assert babel.format_datetime(d, 'long') == \
            '12. April 2010 15:46:00 MESZ'

def test_custom_formats(app, b):
    app.config.update(
        BABEL_DEFAULT_LOCALE='en_US',
        BABEL_DEFAULT_TIMEZONE='Pacific/Johnston'
    )
    b.date_formats['datetime'] = 'long'
    b.date_formats['datetime.long'] = 'MMMM d, yyyy h:mm:ss a'
    d = datetime(2010, 4, 12, 13, 46)

    with app.test_request_context():
        assert babel.format_datetime(d) == 'April 12, 2010 3:46:00 AM'

def test_custom_locale_selector(app, b):
    d = datetime(2010, 4, 12, 13, 46)

    the_timezone = 'UTC'
    the_locale = 'en_US'

    @b.localeselector
    def select_locale():
        return the_locale
    @b.timezoneselector
    def select_timezone():
        return the_timezone

    with app.test_request_context():
        assert babel.format_datetime(d) == 'Apr 12, 2010, 1:46:00 PM'

    the_locale = 'de_DE'
    the_timezone = 'Europe/Vienna'

    with app.test_request_context():
        assert babel.format_datetime(d) == '12.04.2010 15:46:00'

def test_refreshing(app, b):
    d = datetime(2010, 4, 12, 13, 46)
    with app.test_request_context():
        assert babel.format_datetime(d) == 'Apr 12, 2010, 1:46:00 PM'
        app.config['BABEL_DEFAULT_TIMEZONE'] = 'Europe/Vienna'
        babel.refresh()
        assert babel.format_datetime(d) == 'Apr 12, 2010, 3:46:00 PM'


def test_number_formatting_basics(app, b):
    n = 1099

    with app.test_request_context():
        assert babel.format_number(n) == u'1,099'
        assert babel.format_decimal(Decimal('1010.99')) == u'1,010.99'
        assert babel.format_currency(n, 'USD') == '$1,099.00'
        assert babel.format_percent(0.19) == '19%'
        assert babel.format_scientific(10000) == u'1E4'