# coding=utf-8
import sys
import random

from PySide.QtGui import (QApplication)

from ScreamingMercury import (ScreamingMercury)

if __name__ == '__main__':
    # noinspection PyTypeChecker,PyCallByClass
    QApplication.setStyle(u'plastique')
    app = QApplication(sys.argv)

    random.seed()

    screaming_mercury = ScreamingMercury()
    screaming_mercury.show()

    sys.exit(app.exec_())
