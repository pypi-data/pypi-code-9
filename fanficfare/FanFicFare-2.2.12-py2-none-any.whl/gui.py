# -*- coding: utf-8 -*-

# Copyright 2015 Fanficdownloader team, 2015 FanFicFare team
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from optparse import OptionParser
from os.path import expanduser, join, dirname
from os import access, R_OK
from subprocess import call
import ConfigParser
import getpass
import logging
import pprint
import string
import sys

import urllib
import email

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QLabel, QWidget

from PyQt4.Qt import (QDialog, QTableWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                      QPushButton, QFont, QLabel, QCheckBox, QIcon, QLineEdit,
                      QComboBox, QProgressDialog, QTimer, QDialogButtonBox,
                      QPixmap, Qt, QAbstractItemView, QTextEdit, pyqtSignal,
                      QGroupBox, QFrame, QTextBrowser, QSize, QAction)


if sys.version_info < (2, 5):
    print 'This program requires Python 2.5 or newer.'
    sys.exit(1)

if sys.version_info >= (2, 7):
    # suppresses default logger.  Logging is setup in fanficdownload/__init__.py so it works in calibre, too.
    rootlogger = logging.getLogger()
    loghandler = logging.NullHandler()
    loghandler.setFormatter(logging.Formatter('(=====)(levelname)s:%(message)s'))
    rootlogger.addHandler(loghandler)

try:
    # running under calibre
    from calibre_plugins.fanfictiondownloader_plugin.fanficfare import adapters, writers, exceptions
    from calibre_plugins.fanfictiondownloader_plugin.fanficfare.configurable import Configuration
    from calibre_plugins.fanfictiondownloader_plugin.fanficfare.epubutils import (
        get_dcsource_chaptercount, get_update_data, reset_orig_chapters_epub)
    from calibre_plugins.fanfictiondownloader_plugin.fanficfare.geturls import get_urls_from_page, get_urls_from_html, get_urls_from_text
except ImportError:
    from fanficfare import adapters, writers, exceptions
    from fanficfare.configurable import Configuration
    from fanficfare.epubutils import (
        get_dcsource_chaptercount, get_update_data, reset_orig_chapters_epub)
    from fanficfare.geturls import get_urls_from_page, get_urls_from_html, get_urls_from_text


def write_story(config, adapter, writeformat, metaonly=False, outstream=None):
    writer = writers.getWriter(writeformat, config, adapter)
    writer.writeStory(outstream=outstream, metaonly=metaonly)
    output_filename = writer.getOutputFileName()
    del writer
    return output_filename


def main(argv=None, parser=None, passed_defaultsini=None, passed_personalini=None):
    if argv is None:
        argv = sys.argv[1:]
    # read in args, anything starting with -- will be treated as --<varible>=<value>
    if not parser:
        parser = OptionParser('usage: %prog [options] storyurl')
    parser.add_option('-f', '--format', dest='format', default='epub',
                      help='write story as FORMAT, epub(default), mobi, text or html', metavar='FORMAT')

    if passed_defaultsini:
        config_help = 'read config from specified file(s) in addition to calibre plugin personal.ini, ~/.fanficfare/personal.ini, and ./personal.ini'
    else:
        config_help = 'read config from specified file(s) in addition to ~/.fanficfare/defaults.ini, ~/.fanficfare/personal.ini, ./defaults.ini, and ./personal.ini'
    parser.add_option('-c', '--config',
                      action='append', dest='configfile', default=None,
                      help=config_help, metavar='CONFIG')
    parser.add_option('-b', '--begin', dest='begin', default=None,
                      help='Begin with Chapter START', metavar='START')
    parser.add_option('-e', '--end', dest='end', default=None,
                      help='End with Chapter END', metavar='END')
    parser.add_option('-o', '--option',
                      action='append', dest='options',
                      help='set an option NAME=VALUE', metavar='NAME=VALUE')
    parser.add_option('-m', '--meta-only',
                      action='store_true', dest='metaonly',
                      help='Retrieve metadata and stop.  Or, if --update-epub, update metadata title page only.', )
    parser.add_option('-u', '--update-epub',
                      action='store_true', dest='update',
                      help='Update an existing epub with new chapters, give epub filename instead of storyurl.', )
    parser.add_option('--unnew',
                      action='store_true', dest='unnew',
                      help='Remove (new) chapter marks left by mark_new_chapters setting.', )
    parser.add_option('--update-cover',
                      action='store_true', dest='updatecover',
                      help='Update cover in an existing epub, otherwise existing cover (if any) is used on update.  Only valid with --update-epub.', )
    parser.add_option('--force',
                      action='store_true', dest='force',
                      help='Force overwrite of an existing epub, download and overwrite all chapters.', )
    parser.add_option('-i', '--infile',
                      help='Give a filename to read for URLs (and/or existing EPUB files with -u for updates).',
                      dest='infile', default=None,
                      metavar='INFILE')
    parser.add_option('-l', '--list',
                      action='store_true', dest='list',
                      help='Get list of valid story URLs from page given.', )
    parser.add_option('-n', '--normalize-list',
                      action='store_true', dest='normalize', default=False,
                      help='Get list of valid story URLs from page given, but normalized to standard forms.', )
    parser.add_option('-s', '--sites-list',
                      action='store_true', dest='siteslist', default=False,
                      help='Get list of valid story URLs examples.', )
    parser.add_option('-d', '--debug',
                      action='store_true', dest='debug',
                      help='Show debug output while downloading.', )

    options, args = parser.parse_args(argv)

    if not options.debug:
        logger = logging.getLogger('fanficfare')
        logger.setLevel(logging.INFO)

    if not (options.siteslist or options.infile) and len(args) != 1:
        parser.error('incorrect number of arguments')

    if options.siteslist:
        for site, examples in adapters.getSiteExamples():
            print '\n#### %s\nExample URLs:' % site
            for u in examples:
                print '  * %s' % u
        return

    if options.update and options.format != 'epub':
        parser.error('-u/--update-epub only works with epub')

    if options.unnew and options.format != 'epub':
        parser.error('--unnew only works with epub')

    # for passing in a file list
    if options.infile:
        urls=[]
        with open(options.infile,"r") as infile:
            #print "File exists and is readable"
          
            #fileurls = [line.strip() for line in infile]
            for url in infile:
                url = url[:url.find('#')].strip()
                if len(url) > 0:
                    #print "URL: (%s)"%url
                    urls.append(url)
    else:
        urls = args

    if len(urls) > 1:
        for url in urls:
            try:
                do_download(url,
                            options,
                            passed_defaultsini,
                            passed_personalini)
            except Exception, e:
                print "URL(%s) Failed: Exception (%s). Run URL individually for more detail."%(url,e)
    else:
        do_download(urls[0],
                    options,
                    passed_defaultsini,
                    passed_personalini)

# make rest a function and loop on it.
def do_download(arg,
                #options,
                passed_defaultsini=None,
                passed_personalini=None):
                
    # Attempt to update an existing epub.
    chaptercount = None
    output_filename = None

    # if options.unnew:
    #     # remove mark_new_chapters marks
    #     reset_orig_chapters_epub(arg,arg)
    #     return

    url = arg
    # if options.update:
    #     try:
    #         url, chaptercount = get_dcsource_chaptercount(arg)
    #         if not url:
    #             print 'No story URL found in epub to update.'
    #             return
    #         print 'Updating %s, URL: %s' % (arg, url)
    #         output_filename = arg
    #     except Exception:
    #         # if there's an error reading the update file, maybe it's a URL?
    #         # we'll look for an existing outputfile down below.
    #         url = arg
    # else:
    #     url = arg
        
    try:
        configuration = Configuration(adapters.getConfigSectionsFor(url), 'epub')#options.format)
    except exceptions.UnknownSite, e:
        # if options.list or options.normalize:
        #     # list for page doesn't have to be a supported site.
        #     configuration = Configuration('test1.com', options.format)
        # else:
        raise e

    conflist = []
    homepath = join(expanduser('~'), '.fanficdownloader')
    ## also look for .fanficfare now, give higher priority than old dir.
    homepath2 = join(expanduser('~'), '.fanficfare')

    if passed_defaultsini:
        configuration.readfp(passed_defaultsini)

    # don't need to check existance for our selves.
    conflist.append(join(dirname(__file__), 'defaults.ini'))
    conflist.append(join(homepath, 'defaults.ini'))
    conflist.append(join(homepath2, 'defaults.ini'))
    conflist.append('defaults.ini')

    if passed_personalini:
        configuration.readfp(passed_personalini)

    conflist.append(join(homepath, 'personal.ini'))
    conflist.append(join(homepath2, 'personal.ini'))
    conflist.append('personal.ini')

    # if options.configfile:
    #     conflist.extend(options.configfile)

    logging.debug('reading %s config file(s), if present' % conflist)
    configuration.read(conflist)

    try:
        configuration.add_section('overrides')
    except ConfigParser.DuplicateSectionError:
        pass

    # if options.force:
    #     configuration.set('overrides', 'always_overwrite', 'true')

    # if options.update and chaptercount:
    #     configuration.set('overrides', 'output_filename', output_filename)

    # if options.update and not options.updatecover:
    #     configuration.set('overrides', 'never_make_cover', 'true')

    # # images only for epub, even if the user mistakenly turned it
    # # on else where.
    # if options.format not in ('epub', 'html'):
    #     configuration.set('overrides', 'include_images', 'false')

    # if options.options:
    #     for opt in options.options:
    #         (var, val) = opt.split('=')
    #         configuration.set('overrides', var, val)

    # if options.list or options.normalize:
    #     retlist = get_urls_from_page(arg, configuration, normalize=options.normalize)
    #     print '\n'.join(retlist)
    #     return

    try:
        adapter = adapters.getAdapter(configuration, url)
        # adapter.setChaptersRange(options.begin, options.end)

        # check for updating from URL (vs from file)
        # if options.update and not chaptercount:
        #     try:
        #         writer = writers.getWriter('epub', configuration, adapter)
        #         output_filename = writer.getOutputFileName()
        #         noturl, chaptercount = get_dcsource_chaptercount(output_filename)
        #         print 'Updating %s, URL: %s' % (output_filename, url)
        #     except Exception:
        #         options.update = False
        #         pass

        # Check for include_images without no_image_processing. In absence of PIL, give warning.
        if adapter.getConfig('include_images') and not adapter.getConfig('no_image_processing'):
            try:
                from calibre.utils.magick import Image

                logging.debug('Using calibre.utils.magick')
            except ImportError:
                try:
                    import Image

                    logging.debug('Using PIL')
                except ImportError:
                    print "You have include_images enabled, but Python Image Library(PIL) isn't found.\nImages will be included full size in original format.\nContinue? (y/n)?"
                    if not sys.stdin.readline().strip().lower().startswith('y'):
                        return

        # three tries, that's enough if both user/pass & is_adult needed,
        # or a couple tries of one or the other
        for x in range(0, 2):
            try:
                adapter.getStoryMetadataOnly()
            except exceptions.FailedToLogin, f:
                if f.passwdonly:
                    print 'Story requires a password.'
                else:
                    print 'Login Failed, Need Username/Password.'
                    sys.stdout.write('Username: ')
                    adapter.username = sys.stdin.readline().strip()
                adapter.password = getpass.getpass(prompt='Password: ')
                # print('Login: `%s`, Password: `%s`' % (adapter.username, adapter.password))
            except exceptions.AdultCheckRequired:
                print 'Please confirm you are an adult in your locale: (y/n)?'
                if sys.stdin.readline().strip().lower().startswith('y'):
                    adapter.is_adult = True

        if False:#options.update and not options.force:
            # urlchaptercount = int(adapter.getStoryMetadataOnly().getMetadata('numChapters'))

            # if chaptercount == urlchaptercount and not options.metaonly:
            #     print '%s already contains %d chapters.' % (output_filename, chaptercount)
            # elif chaptercount > urlchaptercount:
            #     print '%s contains %d chapters, more than source: %d.' % (output_filename, chaptercount, urlchaptercount)
            # elif chaptercount == 0:
            #     print "%s doesn't contain any recognizable chapters, probably from a different source.  Not updating." % output_filename
            # else:
            #     # update now handled by pre-populating the old
            #     # images and chapters in the adapter rather than
            #     # merging epubs.
            #     (url,
            #      chaptercount,
            #      adapter.oldchapters,
            #      adapter.oldimgs,
            #      adapter.oldcover,
            #      adapter.calibrebookmark,
            #      adapter.logfile,
            #      adapter.oldchaptersmap,
            #      adapter.oldchaptersdata) = (get_update_data(output_filename))[0:9]

            #     print 'Do update - epub(%d) vs url(%d)' % (chaptercount, urlchaptercount)

            #     if not options.update and chaptercount == urlchaptercount and adapter.getConfig('do_update_hook'):
            #         adapter.hookForUpdates(chaptercount)

            #     write_story(configuration, adapter, 'epub')
            pass

        else:
            # regular download
            # if options.metaonly:
            #     pprint.pprint(adapter.getStoryMetadataOnly().getAllMetadata())

            output_filename = write_story(configuration, adapter,
                                          'epub',False)
                                          # options.format, options.metaonly)

        # if not options.metaonly and adapter.getConfig('post_process_cmd'):
        #     metadata = adapter.story.metadata
        #     metadata['output_filename'] = output_filename
        #     call(string.Template(adapter.getConfig('post_process_cmd')).substitute(metadata), shell=True)

        del adapter

    except exceptions.InvalidStoryURL, isu:
        print isu
    except exceptions.StoryDoesNotExist, dne:
        print dne
    except exceptions.UnknownSite, us:
        print us

def _(s):
    return s

class DroppableQTextEdit(QTextEdit):
    def __init__(self,parent):
        QTextEdit.__init__(self,parent)

    def dropEvent(self,event):
        # print("event:%s"%event)

        mimetype='text/uri-list'

        urllist=[]
        filelist="%s"%event.mimeData().data(mimetype)
        for f in filelist.splitlines():
            #print("filename:%s"%f)
            if f.endswith(".eml"):
                fhandle = urllib.urlopen(f)
                #print("file:\n%s\n\n"%fhandle.read())
                msg = email.message_from_file(fhandle)
                if msg.is_multipart():
                    for part in msg.walk():
                        #print("part type:%s"%part.get_content_type())
                        if part.get_content_type() == "text/html":
                            #print("URL list:%s"%get_urls_from_data(part.get_payload(decode=True)))
                            urllist.extend(get_urls_from_html(part.get_payload(decode=True)))
                        if part.get_content_type() == "text/plain":
                            #print("part content:text/plain")
                            # print("part content:%s"%part.get_payload(decode=True))
                            urllist.extend(get_urls_from_text(part.get_payload(decode=True)))
                else:
                    urllist.extend(get_urls_from_text("%s"%msg))
        if urllist:
            self.append("\n".join(urllist))
            return None
        return QTextEdit.dropEvent(self,event)
        
    def canInsertFromMimeData(self, source):
        if source.hasUrls():
            return True
        else:
            return QTextEdit.canInsertFromMimeData(self,source)

    def insertFromMimeData(self, source):
        if source.hasText():
            self.append(source.text())
        else:
            return QTextEdit.insertFromMimeData(self, source)
                            
class LoopProgressDialog(QProgressDialog):
    '''
    ProgressDialog displayed while doing stuff.
    '''
    def __init__(self, gui,
                 book_list,
                 foreach_function,
                 finish_function,
                 init_label=_("Fetching metadata for stories..."),
                 win_title=_("Downloading metadata for stories"),
                 status_prefix=_("Fetched metadata for")):
        QProgressDialog.__init__(self,
                                 init_label,
                                 _('Cancel'), 0, len(book_list), gui)
        self.setWindowTitle(win_title)
        self.setMinimumWidth(500)
        self.book_list = book_list
        self.foreach_function = foreach_function
        self.finish_function = finish_function
        self.status_prefix = status_prefix
        self.i = 0
        self.start_time = datetime.now()

        # can't import at file load.
        # from calibre_plugins.fanficfare_plugin.prefs import prefs
        self.show_est_time = True # prefs['show_est_time']

        ## self.do_loop does QTimer.singleShot on self.do_loop also.
        ## A weird way to do a loop, but that was the example I had.
        QTimer.singleShot(0, self.do_loop)
        self.exec_()

    def updateStatus(self):
        remaining_time_string = ''
        if self.show_est_time and self.i > -1:
            time_spent = (datetime.now() - self.start_time).total_seconds()
            estimated_remaining = (time_spent/(self.i+1)) * len(self.book_list) - time_spent
            remaining_time_string = _(' - %s estimated until done') % ( time_duration_format(estimated_remaining))

        self.setLabelText('%s %d / %d%s' % (self.status_prefix, self.i+1, len(self.book_list), remaining_time_string))
        self.setValue(self.i+1)
        #print(self.labelText())

    def do_loop(self):

        if self.i == 0:
            self.setValue(0)

        book = self.book_list[self.i]
        try:
            ## collision spec passed into getadapter by partial from fff_plugin
            ## no retval only if it exists, but collision is SKIP
            self.foreach_function(book)
            
        # except NotGoingToDownload as d:
        #     book['good']=False
        #     book['comment']=unicode(d)
        #     book['icon'] = d.icon

        except Exception as e:
            book['good']=False
            book['comment']=unicode(e)
            logger.error("Exception: %s:%s"%(book,unicode(e)))
            traceback.print_exc()
            
        self.updateStatus()
        self.i += 1
            
        if self.i >= len(self.book_list) or self.wasCanceled():
            return self.do_when_finished()
        else:
            QTimer.singleShot(0, self.do_loop)

    def do_when_finished(self):
        self.hide()
        # Queues a job to process these books in the background.
        self.finish_function(self.book_list)

def time_duration_format(seconds):
    """
    Convert seconds into a string describing the duration in larger time units (seconds, minutes, hours, days)
    Only returns the two largest time divisions (eg, will drop seconds if there's hours remaining)

    :param seconds: number of seconds
    :return: string description of the duration
    """
    periods = [
        (_('%d day'),_('%d days'),       60*60*24),
        (_('%d hour'),_('%d hours'),     60*60),
        (_('%d minute'),_('%d minutes'), 60),
        (_('%d second'),_('%d seconds'), 1)
        ]

    strings = []
    for period_label, period_plural_label, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds,period_seconds)
            if period_value == 1:
                strings.append( period_label % period_value)
            else:
                strings.append(period_plural_label % period_value)
            if len(strings) == 2:
                break

    if len(strings) == 0:
        return _('less than 1 second')
    else:
        return ', '.join(strings)

        
class FanFicFareGUI(QWidget):
    def __init__(self):
        super(FanFicFareGUI, self).__init__()        
        self.init_gui()
        
    def init_gui(self):
        # self.setGeometry(300, 300, 650, 650)
        self.setMinimumWidth(300)
        self.setWindowTitle('FanFicFare')
        self.setWindowIcon(QIcon('calibre-plugin/images/icon.png'))
        
        self.l = QVBoxLayout()
        self.setLayout(self.l)

        self.toplabel=QLabel('Story URLs, one per line:')
        self.l.addWidget(self.toplabel)

        self.url = DroppableQTextEdit(self)
        self.url.setToolTip('URLs for stories, one per line.\nWill take URLs from clipboard, but only valid URLs.\nAdd [1,5] after the URL to limit the download to chapters 1-5.')
        self.url.setLineWrapMode(QTextEdit.NoWrap)
        self.l.addWidget(self.url)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok) # | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.ok_clicked)
        # self.button_box.rejected.connect(self.reject)
        self.l.addWidget(self.button_box)        
        
        self.show()

    def is_good_downloader_url(self,url):
        return adapters.getNormalStoryURL(url)
        
    def ok_clicked(self):
        print("download %s"%self.get_urlstext())
        url_list = split_text_to_urls(self.get_urlstext())

        for url in url_list:
            do_download(url)
        
        # 
        # books = self.convert_urls_to_books(url_list)

        # # book_list = [ {'url':x} for x in self.get_urlstext().split(
                
        # LoopProgressDialog(self,
        #                    book_list,
        #                    partial(self.get_list_story_urls_loop, db=self.gui.current_db),
        #                    self.get_list_story_urls_finish,
        #                    init_label=_("Collecting URLs for stories..."),
        #                    win_title=_("Get URLs for stories"),
        #                    status_prefix=_("URL retrieved"))

        

    def get_urlstext(self):
        return unicode(self.url.toPlainText())

    # Can't make book a class because it needs to be passed into the
    # bg jobs and only serializable things can be.
    def make_book(self):
        book = {}
        book['title'] = 'Unknown'
        book['author_sort'] = book['author'] = ['Unknown'] # list
        book['comments'] = '' # note this is the book comments.

        book['good'] = True
        book['calibre_id'] = None
        book['begin'] = None
        book['end'] = None
        book['comment'] = '' # note this is a comment on the d/l or update.
        book['url'] = ''
        book['site'] = ''
        book['added'] = False
        book['pubdate'] = None
        return book

    def convert_urls_to_books(self, urls):
        books = []
        uniqueurls = set()
        for i, url in enumerate(urls):
            book = self.convert_url_to_book(url)
            if book['url'] in uniqueurls:
                book['good'] = False
                book['comment'] = "Same story already included."
            uniqueurls.add(book['url'])
            book['listorder']=i # BG d/l jobs don't come back in order.
                                # Didn't matter until anthologies & 'marked' successes
            books.append(book)
        return books

    def convert_url_to_book(self, url):
        book = self.make_book()
        # look here for [\d,\d] at end of url, and remove?
        mc = re.match(r"^(?P<url>.*?)(?:\[(?P<begin>\d+)?(?P<comma>[,-])?(?P<end>\d+)?\])?$",url)
        #print("url:(%s) begin:(%s) end:(%s)"%(mc.group('url'),mc.group('begin'),mc.group('end')))
        url = mc.group('url')
        book['begin'] = mc.group('begin')
        book['end'] = mc.group('end')
        if book['begin'] and not mc.group('comma'):
            book['end'] = book['begin']

        self.set_book_url_and_comment(book,url)
        return book
        
    def set_book_url_and_comment(self,book,url):
        if not url:
            book['comment'] = _("No story URL found.")
            book['good'] = False
            book['icon'] = 'search_delete_saved.png'
            book['status'] = _('Not Found')
        else:
            # get normalized url or None.
            urlsitetuple = adapters.getNormalStoryURLSite(url)
            if urlsitetuple == None:
                book['url'] = url
                book['comment'] = _("URL is not a valid story URL.")
                book['good'] = False
                book['icon']='dialog_error.png'
                book['status'] = _('Bad URL')
            else:
                (book['url'],book['site'])=urlsitetuple

def split_text_to_urls(urls):
    # remove dups while preserving order.
    dups=set()
    def f(x):
        x=x.strip()
        if x and x not in dups:
            dups.add(x)
            return True
        else:
            return False
    return filter(f,urls.strip().splitlines())
        
if __name__ == '__main__':
#    main()
    # Create main app
    qt_app = QApplication(sys.argv)
    
    gui = FanFicFareGUI()
    
    sys.exit(qt_app.exec_())

    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()
    
    
    # # Create a label and set its properties
    # appLabel = QLabel()
    # appLabel.setText("Hello, World!!!\n Traditional first app using PyQt4x")
    # appLabel.setAlignment(Qt.AlignCenter)
    # appLabel.setGeometry(300, 300, 250, 175)

    # # Show the Label
    # appLabel.show()

    # Execute the Application and Exit
    # sys.exit(myApp.exec_())
