import sys
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView, QWebSettings
import gevent


def mainloop(app):
    while True:
        app.processEvents()
        while app.hasPendingEvents():
            app.processEvents()
            gevent.sleep()
        gevent.sleep()
#gevent.spawn(mainloop, QApplication(sys.argv))


class Render(QWebView):
    def __init__(self, url, html=None):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self.settings().setAttribute(QWebSettings.AutoLoadImages, False)
        self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        self.loadFinished.connect(self._loadFinished)
        if html:
            self.page().mainFrame().setHtml(html, QUrl(url))
        else:
            self.page().mainFrame().load(QUrl(url))

    def _loadFinished(self, result):
        print 'loaded'
        self.frame = self.page().mainFrame()
