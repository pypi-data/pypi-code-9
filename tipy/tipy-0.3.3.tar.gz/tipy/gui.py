#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The following can appear on program shutdown:
# QBasicTimer::start: QBasicTimer can only be used with threads started with
# QThread
# There is nothing to worry about it is due to Python GC deleting Qt C++ objects
# in the wrong order.

# If you have any poblem with the ui such as ugly characters font or missing
# menu bar try unseting the environnement variable with :
# $ QT_QPA_PLATFORMTHEME=
# It default value is something like:
# QT_QPA_PLATFORMTHEME=appmenu-qt5
# I can't do much to solve these bugs, it's on Qt side.
# See: https://bugs.launchpad.net/ubuntu/+source/appmenu-qt5/+bug/1307619

"""The program graphical user interface.

@todo 0.0.9:
    Correct the input selection bug.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from logging import StreamHandler, DEBUG
from tipy.db import SqliteDatabaseConnector
from sqlite3 import OperationalError
from tipy.minr import CorpusMiner, DictMiner, FacebookMiner
from tipy.lg import (lg, CNRM, CBLK, CRED, CGRN, CYEL, CBLU, CMAG, CCYN, CWHT,
                     BNRM, BBLK, BRED, BGRN, BYEL, BBLU, BMAG, BCYN, BWHT, BOLD,
                     CF)
from distutils.version import LooseVersion


class LoggerTextEdit(QtWidgets.QTextEdit):
    """A multCSVLine text field showing log messages."""

    def __init__(self, config):
        super(LoggerTextEdit, self).__init__()
        self.pal = QtGui.QPalette()
        textc = QtGui.QColor(255, 255, 255)
        self.pal.setColor(QtGui.QPalette.Text, textc)
        self.setPalette(self.pal)
        self.setReadOnly(True)
        font = QtGui.QFont()
        try:
            font.setPointSize(config.getas('GUI', 'font_size', 'int'))
        except KeyError:
            font.setPointSize(10)
        self.setFont(font)

    def write(self, text):
        """Simulate LogHandler by having a write() method."""
        text = text.replace(CNRM, '<font color="White">')
        text = text.replace(CBLK, '<font color="Gray">')
        text = text.replace(CRED, '<font color="Crimson">')
        text = text.replace(CGRN, '<font color="LimeGreen">')
        text = text.replace(CYEL, '<font color="Gold">')
        text = text.replace(CBLU, '<font color="RoyalBlue ">')
        text = text.replace(CMAG, '<font color="DeepPink ">')
        text = text.replace(CCYN, '<font color="MediumAquaMarine ">')
        text = text.replace(CWHT, '<font color="White">')
        text = text.replace(BNRM, '<b><font color="White"></b>')
        text = text.replace(BBLK, '<b><font color="Gray"></b>')
        text = text.replace(BRED, '<b><font color="Crimson"></b>')
        text = text.replace(BGRN, '<b><font color="LimeGreen"></b>')
        text = text.replace(BYEL, '<b><font color="Gold"></b>')
        text = text.replace(BBLU, '<b><font color="RoyalBlue "></b>')
        text = text.replace(BMAG, '<b><font color="DeepPink "></b>')
        text = text.replace(BCYN, '<b><font color="MediumAquaMarine "></b>')
        text = text.replace(BWHT, '<b><font color="White"></b>')
        text = text.replace(BOLD, '<b></b>')
        text = text.replace('\n', '<br>')
        text = text + '</font>'
        self.insertHtml(text)


class LogDockWidget(QtWidgets.QDockWidget):
    """A main window dockable widget showing the app logs."""

    def __init__(self, config):
        super(LogDockWidget, self).__init__('log')
        self.setWidget(LoggerTextEdit(config))
        self.handler = StreamHandler(self.widget())
        self.handler.setLevel(DEBUG)
        self.handler.setFormatter(CF)
        lg.addHandler(self.handler)

    def setColor(self, fg, bg):
        """Set the background color of the log window."""
        self.widget().setStyleSheet("color: %s;background-color: %s" % (fg, bg))


class MainWindow(QtWidgets.QMainWindow):
    """The main window of the graphical user interface.

    G{classtree MainWindow}
    """

    CORPUS_NGRAM_PREDICTOR = 0
    USER_SMOOTH_NGRAM_PREDICTOR = 1
    FB_SMOOTH_NGRAM_PREDICTOR = 2
    LAST_OCCUR_PREDICTOR = 3
    MEMORIZE_PREDICTOR = 4
    DICTIONARY_PREDICTOR = 5
    TEXT_FILE_MINER = 0
    DICTIONARY_MINER = 1
    FACEBOOK_MINER = 2
    TWITTER_MINER = 3

    def __init__(self, driver):
        """MainWindow creator.

        It allow the user to:
            - Type text and get predictive suggestions.
            - Directly complete input words or insert predicted words in the
              input.
            - See the miners informations.
            - Execute mining operations using the defined miners.
            - Delete miners database.
            - Modify almost every options of the configuration file using the
              settings window.

        @param driver:
            The Driver instance wich contains everything needed for word
            prediction.
        @type driver: L{Driver}
        """
        super(MainWindow, self).__init__()
        self.driver = driver
        self.config = self.driver.configuration
        self.predictors = [
            'CorpusNgramPredictor',
            'InputNgramPredictor',
            'FbNgramPredictor',
            'LateOccurPredictor',
            'MemorizePredictor',
            'DictionaryPredictor']
        self.miners = [
            'CorpusMiner',
            'DictMiner',
            'FbMiner',
            'TwitterMiner']
        self.prevText = ''
        self.prevCursorPosition = 0
        self.prevTextLen = 0
        self.dbPath = '[UNDEFINED]'
        self.nGramSize = '[UNDEFINED]'
        self.predsUsingDb = []
        self.setupUi(self)
        self.mainTabs.setCurrentIndex(1)
        self.on_miner_selected(self.minersComboBox.currentIndex())

    def setupUi(self, MainWindow):
        """Create and set the main window widgets and layouts."""
        MainWindow.resize(640, 510)
        MainWindow.setWindowTitle('Preditor')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.mainTabs = QtWidgets.QTabWidget(self.centralwidget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        ############################## MINING TAB ##############################
        self.miningTab = QtWidgets.QWidget()
        self.gridLayout_5 = QtWidgets.QGridLayout(self.miningTab)
        # =================== DATABASE STATISTICS GROUP BOX ================== #
        self.dbStatsGroupBox = QtWidgets.QGroupBox(self.miningTab)
        self.dbStatsGroupBox.setTitle('Miner\'s database statistics')
        self.gridLayout_6 = QtWidgets.QGridLayout(self.dbStatsGroupBox)
        # Path label
        self.dbPathLabel = QtWidgets.QLabel(self.dbStatsGroupBox)
        self.dbPathLabel.setText('Path:')
        # Path value label
        self.dbPathValueLabel = QtWidgets.QLabel(self.dbStatsGroupBox)
        self.dbPathValueLabel.setText('-')
        # n-grams size label
        self.ngramsSizeLabel = QtWidgets.QLabel(self.dbStatsGroupBox)
        self.ngramsSizeLabel.setText('N-grams size:')
        # n-grams size value label
        self.ngramsSizeValueLabel = QtWidgets.QLabel(self.dbStatsGroupBox)
        self.ngramsSizeValueLabel.setText('-')
        # Number of n-grams label
        self.noNgramsLabel = QtWidgets.QLabel(self.dbStatsGroupBox)
        self.noNgramsLabel.setText('Number of n-grams:')
        # Table associating n-grams size value and n-grams count
        self.ngramsTable = QtWidgets.QTableWidget(self.dbStatsGroupBox)
        self.ngramsTable.setColumnCount(2)
        self.ngramsTable.setHorizontalHeaderItem(
            0, QtWidgets.QTableWidgetItem())
        self.ngramsTable.setHorizontalHeaderItem(
            1, QtWidgets.QTableWidgetItem())
        self.ngramsTable.setSortingEnabled(True)
        self.ngramsTable.horizontalHeaderItem(0).setText('N-gram size')
        self.ngramsTable.horizontalHeaderItem(1).setText('Number of n-grams')
        # Predictors using the miner database label
        self.predsUsingDbLabel = QtWidgets.QLabel(self.dbStatsGroupBox)
        self.predsUsingDbLabel.setText('Predictors using the database:')
        # List of predictors using the miner database as input
        self.predsUsingDbList = QtWidgets.QListWidget(self.dbStatsGroupBox)
        # ==================== MINING OPERATIONS GROUP BOX =================== #
        self.miningGroupBox = QtWidgets.QGroupBox(self.miningTab)
        self.miningGroupBox.setTitle('Mining operations')
        self.gridLayout_2 = QtWidgets.QGridLayout(self.miningGroupBox)
        # A comboBox to select between available miners
        self.minersComboBox = QtWidgets.QComboBox(self.miningGroupBox)
        for miner in self.miners:
            self.minersComboBox.addItem(miner)
        self.minersComboBox.currentIndexChanged.connect(self.on_miner_selected)
        # Operation status label
        self.minerOperationLabel = QtWidgets.QLabel(self.miningGroupBox)
        self.minerOperationLabel.setText('Operation:')
        # Operation status value label
        self.minerOperationValueLabel = QtWidgets.QLabel(self.miningGroupBox)
        self.minerOperationValueLabel.setText('-')
        # Operation progression label
        self.progressLabel = QtWidgets.QLabel(self.miningGroupBox)
        self.progressLabel.setText('Progression:')
        # Operation progress bar
        self.progressBar = QtWidgets.QProgressBar(self.miningGroupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setRange(0, 100)
        # Delete database file button
        self.deleteDbBtn = QtWidgets.QPushButton(self.miningGroupBox)
        self.deleteDbBtn.setText('Delete database file')
        self.deleteDbBtn.released.connect(self.on_rm_db_btn_released)
        # Run mining operation button
        self.mineBtn = QtWidgets.QPushButton(self.miningGroupBox)
        self.mineBtn.setText('MINE !')
        self.mineBtn.released.connect(self.on_mine_btn_released)
        ############################ PREDICTING TAB ############################
        self.predictingTab = QtWidgets.QWidget()
        self.gridLayout_4 = QtWidgets.QGridLayout(self.predictingTab)
        self.inputTextEdit = QtWidgets.QPlainTextEdit(self.predictingTab)
        #~ self.inputTextEdit.textChanged.connect(self.on_input_text_change)
        self.inputTextEdit.cursorPositionChanged.connect(
            self.on_input_text_cursor_position_change)
        self.suggestionsList = QtWidgets.QListWidget(self.predictingTab)
        self.suggestionsList.itemDoubleClicked.connect(
            self.on_suggestion_double_clicked)
        ######################### TABS CONTENT AND NAME ########################
        self.mainTabs.addTab(self.miningTab, '')
        self.mainTabs.addTab(self.predictingTab, '')
        self.mainTabs.setTabText(
            self.mainTabs.indexOf(self.miningTab), 'Mining')
        self.mainTabs.setTabText(
            self.mainTabs.indexOf(self.predictingTab), 'Predicting')
        ###################### ADD EVERYTHING TO LAYOUTS #######################
        self.horizontalLayout.addWidget(self.deleteDbBtn)
        self.horizontalLayout.addWidget(self.mineBtn)
        self.gridLayout_2.addWidget(self.minersComboBox, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.minerOperationLabel, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.progressLabel, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.progressBar, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.minerOperationValueLabel, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.minerOperationValueLabel, 0, 1, 1, 1)
        self.gridLayout_5.addWidget(self.miningGroupBox, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.inputTextEdit, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.mainTabs, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.noNgramsLabel, 6, 0, 1, 1)
        self.gridLayout_7.addWidget(self.dbPathLabel, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.ngramsSizeLabel, 1, 0, 1, 1)
        self.gridLayout_7.addWidget(self.dbPathValueLabel, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.ngramsSizeValueLabel, 1, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.predsUsingDbLabel, 1, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_8, 2, 0, 1, 1)
        self.gridLayout_6.addWidget(self.ngramsTable, 7, 0, 1, 1)
        self.gridLayout_5.addWidget(self.dbStatsGroupBox, 3, 0, 1, 1)
        self.gridLayout_6.addWidget(self.predsUsingDbList, 2, 0, 1, 1)
        self.gridLayout_5.addWidget(self.dbStatsGroupBox, 3, 0, 1, 1)
        self.gridLayout_4.addWidget(self.suggestionsList, 1, 0, 1, 1)
        ################################ MENUBAR ###############################
        # The menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 18))
        # ============================= THE MENUS ============================ #
        # The File menu
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle('File')
        # The Edition menu
        self.menuEdition = QtWidgets.QMenu(self.menubar)
        self.menuEdition.setTitle('Edition')
        # The View menu
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setTitle('View')
        # =========================== THE ACTIONS ============================ #
        # The Open action
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setText('Import some text...')
        # The Quit action
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setText('Quit')
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionQuit.triggered.connect(
            QtCore.QCoreApplication.instance().quit)
        # The Paste action
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setText('Paste')
        self.actionPaste.setShortcut('Ctrl+V')
        self.actionPaste.triggered.connect(self.on_paste_btn_triggered)
        # The Copy action
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setText('Copy')
        self.actionCopy.setShortcut('Ctrl+C')
        self.actionCopy.triggered.connect(self.on_copy_btn_triggered)
        # The Cut action
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setText('Cut')
        self.actionCut.setShortcut('Ctrl+X')
        self.actionCut.triggered.connect(self.on_cut_btn_triggered)
        # The Settings action
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setText('Preferences')
        self.actionSettings.setShortcut('Ctrl+Alt+P')
        self.actionSettings.triggered.connect(self.on_pref_triggered)
        # The Afficher les probabilités action
        self.actionShowProbabilities = QtWidgets.QAction(MainWindow)
        self.actionShowProbabilities.setText('Show probabilities')
        self.actionShowProbabilities.triggered.connect(
            self.on_show_probabilities_triggered)
        self.actionShowProbabilities.setCheckable(True)
        # ===================== PUTTING IT ALL TOGETHER ====================== #
        # Add the actions to the File menu
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        # Add the actions to the Edition menu
        self.menuEdition.addAction(self.actionCut)
        self.menuEdition.addAction(self.actionCopy)
        self.menuEdition.addAction(self.actionPaste)
        self.menuEdition.addSeparator()
        self.menuEdition.addAction(self.actionSettings)
        # Add the actions to the View menu
        self.menuView.addAction(self.actionShowProbabilities)
        # Add the menus to the menubar
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdition.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        # Set the menubar
        MainWindow.setMenuBar(self.menubar)
        ############################### STATUSBAR ##############################
        # The statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # Set the statusbar
        MainWindow.setStatusBar(self.statusbar)
        ############################ LOG DOCK WIDGET ###########################
        # The dock widget for the log
        self.logDock = LogDockWidget(self.config)
        self.logDock.setColor('white', 'black')
        # Set the dock
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.logDock)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # Show something
        lg.info('Session starts.')

    def on_paste_btn_triggered(self, checked=False):
        """Paste what's inside the clipboard."""
        self.inputTextEdit.paste()

    def on_copy_btn_triggered(self, checked=False):
        """Copy the selection."""
        self.inputTextEdit.copy()

    def on_cut_btn_triggered(self, checked=False):
        """Cut the selection."""
        self.inputTextEdit.cut()

    def on_show_probabilities_triggered(self, checked=False):
        """Show the suggested words probabilities."""
        lg.warning('Not yet implemented.')

    def on_pref_triggered(self, checked=False):
        """Open the settings dialog."""
        settingsDialog = stngs.Settings_UI(self.config)
        settingsDialog.exec_()
        self.write_config()

    def write_config(self):
        """Write the current configuration in the configuration file."""
        if self.driver.configFile:
            with open(self.driver.configFile, 'w') as f:
                self.config.write(f)

    def predictors_using_db(self):
        """Create a list of every predictors name which use a given database.

        @return:
            The list of the predictors using the database file 'self.dbPath'.
        @rtype: list
        """
        predsUsingDb = []
        for pred in self.predictors:
            try:
                if self.config[pred]['database'] == self.dbPath:
                    predsUsingDb.append(pred)
            except KeyError:
                continue
        return predsUsingDb

    def on_miner_selected(self, miner):
        """Callback called when the user select a miner in the combo box.

        When a miner is selected in the miner selection combo box some settings
        of the miner have to be retrieved from the configuration in order to
        display them to the user using the set_miner_widgets_values() method.
        As every miners store their results (n-grams) in a database the database
        path and the n-gram size are retrieved from the configuration and stored
        into the "dbPath" and "nGramSize" instance variables.

        @param miner:
            The index of the miner in the combo box.
        @type miner: int
        """
        if miner == self.TEXT_FILE_MINER:
            self.dbPath = self.config.getas('CorpusMiner', 'database')
            self.nGramSize = self.config.getas('CorpusMiner', 'n')
            self.predsUsingDb = self.predictors_using_db()
        elif miner == self.DICTIONARY_MINER:
            self.dbPath = self.config.getas('DictMiner', 'database')
            self.nGramSize = '1'
            self.predsUsingDb = self.predictors_using_db()
        elif miner == self.FACEBOOK_MINER:
            self.dbPath = self.config.getas('FbMiner', 'database')
            self.nGramSize = self.config.getas('FbMiner', 'n')
            self.predsUsingDb = self.predictors_using_db()
        elif miner == self.TWITTER_MINER:
            self.dbPath = '[UNDEFINED]'
            self.nGramSize = '[UNDEFINED]'
        else:
            self.dbPath = '[UNDEFINED]'
            self.nGramSize = '[UNDEFINED]'
        self.set_miner_widgets_values()

    def set_miner_widgets_values(self):
        """Update the widgets (labels and list) displaying infos on the miner.

        When a miner is selected in the miner selection combo box, its config
        settings are retrieve from the configuration and the instance variables
        "dbPath", "nGramSize" and "predsUsingDb" are set.
        This method modify the value of the widgets displaying the informations
        about the miner with the above-mentioned variables.
        """
        nGramCount = []
        self.dbPathValueLabel.setText(self.dbPath)
        self.ngramsSizeValueLabel.setText(self.nGramSize)
        while self.predsUsingDbList.count():
            self.predsUsingDbList.takeItem(0)
        for pred in self.predictors:
            if pred in self.predsUsingDb:
                self.predsUsingDbList.addItem(pred)
        if self.nGramSize == '[UNDEFINED]' or self.dbPath == '[UNDEFINED]':
            self.ngramsTable.setRowCount(0)
            return
        database = SqliteDatabaseConnector(self.dbPath, self.nGramSize)
        for n in range(1, int(self.nGramSize) + 1):
            try:
                nGramCount.append(database.ngrams_in_table(n))
            except OperationalError:
                nGramCount.append(0)
        database.close_database()
        self.ngramsTable.setRowCount(n)
        for i, count in enumerate(nGramCount):
            self.ngramsTable.setItem(
                i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
            self.ngramsTable.setItem(
                i, 1, QtWidgets.QTableWidgetItem(str(count)))

    def progress_callback(self, perc=0, text=None):
        """Update the label showing the mining operation and the progress bar.

        This method is a callback which is called from the miners. It update the
        text of the label displaying the minig operation and the value of the
        progress bar displaying the operation progression.

        @param perc:
            Computed by the miners calling the callback, it indicate the
            operation progression and is usually a float but it must be
            converted to int as the progress bar only show integers.
        @type perc: float or int
        @param text:
            The text to display in the mining operation label.
        @type text: str
        """
        if text:
            self.minerOperationValueLabel.setText(text)
            self.minerOperationValueLabel.repaint()
        self.progressBar.setValue(round(perc))

    def on_rm_db_btn_released(self):
        """Callback called when the user press the "Delete database" button.

        The method first identify the current miner selected in the combo box
        using its index then create an instance of this miner and called its
        rm_db() method to effectively carry out the database suppression
        operation.
        Some miners modify the configuration so the config file needs to be
        rewrite after the operation.
        Here is a short description of the miners database suppression
        operation, please refer to their rm_db() method docstring for more
        informations:
            - CorpusMiner: Remove the database file.
            - FbMiner: Remove the database file and set the "last_update" config
              option to the minimum value so the config have to be writen
              afterward.
        """
        if self.minersComboBox.currentIndex() == self.TEXT_FILE_MINER:
            miner = CorpusMiner(self.config, 'CorpusMiner')
            miner.rm_db()
        elif self.minersComboBox.currentIndex() == self.DICTIONARY_MINER:
            miner = DictMiner(self.config, 'DictMiner')
            miner.rm_db()
        elif self.minersComboBox.currentIndex() == self.FACEBOOK_MINER:
            miner = FacebookMiner(self.config, 'FbMiner')
            miner.rm_db()
            self.write_config()
        elif self.minersComboBox.currentIndex() == self.TWITTER_MINER:
            self.progress_callback(0, 'error: [MINER NOT IMPLEMENTED YET]')
            lg.error('Miner not implemented yet')
            return
        else:   # should never happen
            self.progress_callback(0, 'error: unknown miner')
            lg.error('Unknown miner "{0}"'.format(
                self.minersComboBox.currentIndex()))
            return
        self.set_miner_widgets_values()

    def on_mine_btn_released(self):
        """Callback called when the user press the "MINE!" button.

        The method first identify the current miner selected in the combo box
        using its index then create an instance of this miner and called its
        mine() method to effectively carry out the mining operation.
        Some miners modify the configuration so the config file needs to be
        rewrite after the operation.
        Here is a short description of the miners mining operation, please refer
        to their mine() method docstring for more informations:
            - CorpusMiner: Mine a text corpus (i.e. a set of text files) by
              extracting n-grams from the files and inserting them into a
              database.
            - FbMiner: Mine a facebook user wall (only text messages from
              posts) by extracting n-grams from the posts and inserting them
              into a database. This miner modifies the "last_update" option of
              its config section so the config have to be writen afterward.
            - TwiterMiner: Not implemented yet but it will be very similar to
              FbMiner.
        """
        if self.minersComboBox.currentIndex() == self.TEXT_FILE_MINER:
            miner = CorpusMiner(
                self.config, 'CorpusMiner', self.progress_callback)
            miner.mine()
        elif self.minersComboBox.currentIndex() == self.DICTIONARY_MINER:
            miner = DictMiner(self.config, 'DictMiner', self.progress_callback)
            miner.mine()
        elif self.minersComboBox.currentIndex() == self.FACEBOOK_MINER:
            miner = FacebookMiner(
                self.config, 'FbMiner', self.progress_callback)
            miner.mine()
            self.write_config()
        elif self.minersComboBox.currentIndex() == self.TWITTER_MINER:
            self.progress_callback(0, 'error: [MINER NOT IMPLEMENTED YET]')
            lg.warning('Miner not implemented yet')
            return
        else:   # should never happen
            self.progress_callback(0, 'error: unknown miner')
            lg.warning('Unknown miner')
            return
        self.set_miner_widgets_values()

    def on_input_text_change(self):
        """Update the input buffers and compute the suggestion.

        This method is called whenever one or more character(s) is/are added to
        or removed from the input text. It update the input left and right
        buffers according to the text change and then generate the suggestions
        for the new input context.
        There is three king of input text change:
            - Characters have been appened:
              -> Characters are added to the left input buffer (via
              callback.update()).
            - Part of the characters have been removed:
              -> Characters are removed to the left input buffer (via
              callback.update()). It simulates a backspace input.
            - Every characters have been removed (while new ones have been
              added):
              -> Every characters of the left input buffer are removed (via
              callback.update()). New characters, if any, are added to the left
              input buffer (via callback.update()).
        @note: It correspond to a Ctrl+A then <some printable characters> or
            <backspace>.
        """
        text = self.inputTextEdit.toPlainText()
        if text.startswith(self.prevText):
            change = text[len(self.prevText):]
            self.driver.callback.update(change)
        elif self.prevText.startswith(text):
            self.driver.callback.update('\b', len(self.prevText) - len(text))
        else:
            self.driver.callback.update('\b', len(self.prevText))
            self.driver.callback.update(text)
        self.prevText = text
        self.make_suggestions()

    def make_suggestions(self):
        """Compute and show suggestions.

        Request the PredictorActivator to compute the suggestions and show them
        in the suggestion list.
        """
        self.suggestionsList.clear()
        for p in self.driver.predict():
            self.suggestionsList.addItem(p)

    def on_input_text_cursor_position_change(self):
        """Callback called when the input text cursor position change.

        There's three possible moves types:
            - The cursor moved because one or more character(s) have been added
              to or removed from the input text:
              -> The cursor position and the input text length are saved and the
              suggestions are updated according to the current input.
            - The cursor moved because the user pressed the left arrow key or
              clicked somewhere in the text, on the left of the previous cursor
              position:
              -> In this case the input text has not change we call the Driver
              callback to modify the input left and right buffer so that the
              left buffer now contains what's on the left of the cursor and the
              right buffer now contains what's on the right of the cursor. The
              suggestions are then updated according to the current cursor
              position.
            - The cursor moved because the user pressed the right arrow key or
              clicked somewhere in the text, on the right of the previous cursor
              position:
              -> In this case the input text has not change we call the Driver
              callback to modify the input left and right buffer so that the
              left buffer now contains what's on the left of the cursor and the
              right buffer now contains what's on the right of the cursor. The
              suggestions are then updated according to the current cursor
              position.

        @note: The on_input_text_change() method used to be connected to the
            textChanged signal of the input text widget but it is redundant
            because if the text change, the cursor position automatically change
            too. It save some operations.

        @bug:
            When selecting characters in the input field (self.inputTextEdit)
            the cursor position is modified and induce erroneous context changes
            and word predictions.
        """
        currentCursorPosition = self.inputTextEdit.textCursor().position()
        currentTextLen = len(self.inputTextEdit.toPlainText())
        posDiff = currentCursorPosition - self.prevCursorPosition
        lenDiff = currentTextLen - self.prevTextLen
        if lenDiff == posDiff:              # Char(s) have been added or removed
            self.on_input_text_change()
        elif posDiff < 0 and lenDiff == 0:  # Move cursor to the left
            self.driver.callback.update('\x1B[D', posDiff)
        elif posDiff > 0 and lenDiff == 0:  # Move cursor to the right
            self.driver.callback.update('\x1B[C', posDiff)
        else:                               # Should never happen
            self.prevCursorPosition = currentCursorPosition
            self.prevTextLen = currentTextLen
            return
        self.prevCursorPosition = currentCursorPosition
        self.prevTextLen = currentTextLen
        self.make_suggestions()

    def on_suggestion_double_clicked(self, item):
        """Complete the input with the selected suggestion.

        When the user double click on a word of the list the word is used to
        complete the input text. There is two kind of completion depending on
        the input cursor position:
            - The cursor is at the end of the text:
              -> The completion for the last token is computed and append to the
              input text. A space is then added allowing the user to save a key
              and the program to immediatly suggest the next word prediction.
            - The cursor is not at the end of the text:
              -> The completion for the token in which the cursor is is computed
              and the end of the token is replaced by the completion.

        During this method the input text widget signals are disconnected which
        means that no suggestions will be compute during the completion process.
        This is important because this method will modify the input text but, of
        course, there is no need to generate any suggestions as the user isn't
        typing anything during the process.

        @note: A token can be a word or a separator. If it is a word then the
               completion represents the end of the word. If it is a separator
               then the completion represents the next word.

        @param item:
            The selected item (word) in the suggestion list.
        @type item:
            QtWidgets.QListWidgetItem
        """
        self.inputTextEdit.cursorPositionChanged.disconnect()
        currentCursorPosition = self.inputTextEdit.textCursor().position()
        if currentCursorPosition == len(self.inputTextEdit.toPlainText()):
            completion = self.driver.make_completion(item.text())
            # If the word is finished then suggestion = word and completion = ''
            # But we still have to add a space after the word so check if
            # completion is not False
            if not completion is False:
                self.inputTextEdit.insertPlainText(completion)
                self.driver.callback.update(completion)
                self.prevCursorPosition = \
                    self.inputTextEdit.textCursor().position()
                self.prevTextLen = len(self.inputTextEdit.toPlainText())
                self.prevText = self.inputTextEdit.toPlainText()
                self.inputTextEdit.cursorPositionChanged.connect(
                    self.on_input_text_cursor_position_change)
                self.inputTextEdit.insertPlainText(' ')
        else:
            completion = self.driver.make_completion(item.text())
            if completion:
                suffix = self.driver.contextMonitor.suffix()
                tmpCursor = self.inputTextEdit.textCursor()
                tmpCursor.movePosition(
                    QtQTextCursor.Right,
                    QtQTextCursor.MoveAnchor, len(suffix))
                self.inputTextEdit.setTextCursor(tmpCursor)
                self.driver.callback.update('\x1B[C', len(suffix))
                for i in range(len(suffix)):
                    self.inputTextEdit.textCursor().deletePreviousChar()
                    self.driver.callback.update('\b', 1)
                self.inputTextEdit.insertPlainText(completion)
                self.driver.callback.update(completion)
                self.prevCursorPosition = \
                    self.inputTextEdit.textCursor().position()
                self.prevTextLen = len(self.inputTextEdit.toPlainText())
                self.prevText = self.inputTextEdit.toPlainText()
        self.inputTextEdit.cursorPositionChanged.connect(
            self.on_input_text_cursor_position_change)
