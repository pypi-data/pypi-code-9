from pprint import pprint
from datetime import datetime

__author__ = 'mweilbaecher'

from pyxelletter import Pyxelletter
if __name__ == '__main__':
    p = Pyxelletter('mseibert@seibert-media.net','Vxj6jjvssp7JUTg')

    #pprint(p.get_letters())
    status_dict = p.get_letter_status(10245644)

    pprint(status_dict)

    d = datetime.fromtimestamp(status_dict['dates']['uploaded_at'])

    for time in status_dict['dates'].values():
        if time:
            print datetime.fromtimestamp(time)

    print d