""" Modul for the mensa in rostock"""
import datetime

class CanteenHRO(object):
    """Class for parsing the canteen menus in rostock"""

    # Project Metadata
    __version__ = u'0.0.3'
    __author__ = u'Mathias Perlet'
    __author_email__ = u'mathias@mperlet.de'
    __description__ = u'Parses the menus of the canteens in Rostock.'

    def __init__(self):
        """
            TABLE_NO: 0 is the first table, 1 the second
            CANTEEN_NO: Number between 0 and 6,
                        0 is Mensa_Sued, 1 = Cafe_Einstein, ...see the website
            URL: Source-Url
            FIRST_LABEL: for the food without a caption
        """
        self.TABLE_NO = 0 # 0 is the first table from one canteen, 1 is the next
        self.CANTEEN_NO = 0 # 0 is Mensa_Sued, 1 = Cafe_Einstein, ...see the website
        self.URL = u'http://www.studentenwerk-rostock.de/de/mensen/speiseplaene.html'
        self.FIRST_LABEL = 'Theke 1/2'

        # Initial variables
        self._mensa_name = ''
        self._canteen_table = ''
        self._headline = ''
        self._ret_dict = {}
        self._label = ''
        self._weekday = 0
        self._weekday_str = ''


    def init(self):
        """ Executes the parsing """
        from pyquery import PyQuery
        canteen_url = PyQuery(url=self.URL)
        path_to_canteen = canteen_url("#begin_content > div > dl").eq(self.CANTEEN_NO)

        self._mensa_name = path_to_canteen.find('p').text()
        path_to_canteen = path_to_canteen.find('dd > div > div').eq(0).children()
        self._canteen_table = path_to_canteen.find("table").eq(self.TABLE_NO).children()
        self._headline = path_to_canteen.filter('h3').eq(self.TABLE_NO).text()

        self._label = self.FIRST_LABEL

        # init the first list of food
        self._ret_dict[self._label] = []

        self._weekday = datetime.date.today().weekday()
        _weekday_str = self._canteen_table[0].getchildren()[self._weekday].text
        self._headline = '%s (%s)' % (self._headline, _weekday_str)
        return self


    def _menu_to_dict(self):
        """ Generates a dict with the current canteen menu"""
        # Table to Dict
        for row in self._canteen_table[1:]:
            cols = row.getchildren()[self._weekday]
            children = cols.getchildren()

            if len(children) == 1 and children[0].tag == 'b':
                self._label = children[0].text_content()
                self._ret_dict[self._label] = []
            if cols.text is not None:
                self._ret_dict[self._label].append(cols.text)


    def get_menu(self):
        """Returns the current dict"""
        self._menu_to_dict()
        return self._ret_dict


    def get_headline(self):
        """Returns the headline of the canteen menu e.g."""
        return self._headline


    def get_mensa_name(self):
        """Returns the name of the canteen"""
        return self._mensa_name


    def set_table_no(self, number):
        """Sets the table number, useful is 0 and 1"""
        self.TABLE_NO = number
        return self


    def set_canteen_no(self, number):
        """Sets the canteen number, useful is a number between 0 and 6"""
        self.CANTEEN_NO = number
        return self


    def set_url(self, url):
        """Sets the url"""
        self.URL = url
        return self


    def set_first_label(self, label):
        """Sets the key for food without label"""
        self.FIRST_LABEL = label
        return self
