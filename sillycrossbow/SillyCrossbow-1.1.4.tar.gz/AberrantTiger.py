# encoding: utf8
import sys

from PySide.QtCore import Qt, QRect, QSettings, QDir, QDirIterator

from PySide.QtGui import QApplication, QWidget, QPainter, QImage, QTransform, QFileDialog

from SillyCrossbow import crop_image_from_file
from AberrantTiger import Ui_CropWindow

COMPANY = 'Venus.Games'
APPNAME = 'SillyCrossbow'


# noinspection PyPep8Naming
class CropWidget(QWidget, Ui_CropWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        self.restoreGeometry(self.settings.value(self.__class__.__name__))

        self.images = []

        if len(sys.argv) > 1:
            d = QDir(path=sys.argv[1])
        else:
            d = QDir(path=QFileDialog.getExistingDirectory())

        d.setNameFilters(['*.png'])
        d.setFilter(QDir.Files or QDir.NoDotAndDotDot)

        d = QDirIterator(d)

        images = []

        while d.hasNext():
            images.append(d.next())

        for i in images:
            print i

        self.images = [QImage(i) for i in images]
        self.images += [crop_image_from_file(i, 50)[0] for i in images]

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setWorldTransform(QTransform().scale(0.5, 0.5))

        x = 0

        for i in self.images:
            painter.drawImage(QRect(x, 0, i.width(), i.height()), i)
            painter.drawRect(x, 0, i.width(), i.height())
            x += i.width()

    def closeEvent(self, e):
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, COMPANY, APPNAME)
        self.settings.setValue(self.__class__.__name__, self.saveGeometry())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    push = CropWidget()
    push.show()

    sys.exit(app.exec_())
