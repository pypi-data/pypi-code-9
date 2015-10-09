from pyquery import PyQuery
import datetime

class CanteenHRO(object):

    __version__ = u'0.0.1'
    __author__ = u'Mathias Perlet'
    __author_email__ = u'mathias@mperlet.de'
    __description__ = u'Parses the menus of the canteens in Rostock.'

    TABLE_NO = 0 # 0 is the first table from one canteen, 1 is the next
    CANTEEN_NO = 0 # 0 is Mensa_Sued, 1 = Cafe_Einstein, ...see the website
    URL = u'http://www.studentenwerk-rostock.de/de/mensen/speiseplaene.html'
    FIRST_LABEL = 'Theke 1/2'

    def init(self):
        canteenUrl = PyQuery(url=self.URL)
        path_to_canteen = canteenUrl("#begin_content > div > dl").eq(self.CANTEEN_NO)

        self.mensa_name = path_to_canteen.find('p').text()
        path_to_canteen = path_to_canteen.find('dd > div > div').eq(0).children()
        self.canteen_table = path_to_canteen.find("table").eq(self.TABLE_NO).children()
        self.headline = path_to_canteen.filter('h3').eq(self.TABLE_NO).text()

        self.ret_dict = {}
        self.label = self.FIRST_LABEL

        # init the first list of food
        self.ret_dict[self.label] = []

        self.weekday = datetime.date.today().weekday()
        self.headline = '%s (%s)' % (self.headline,
                            self.canteen_table[0].getchildren()[self.weekday].text)

    def _menu_to_dict(self):
        # Table to Dict
        for row in self.canteen_table[1:]:
            cols = row.getchildren()[self.weekday]
            children = cols.getchildren()

            if len(children) == 1 and children[0].tag == 'b':
                self.label = children[0].text_content()
                self.ret_dict[self.label] = []
            if cols.text is not None:
                self.ret_dict[self.label].append(cols.text)

    def get_menu(self):
        self._menu_to_dict()
        return self.ret_dict

    def get_headline(self):
        return self.headline

    def get_mensa_name(self):
        return self.mensa_name
