#!/usr/bin/env python3

"""The settings dialog window allow the user to access the configuration.

The settings allow the user to consult and modify almost every configuration
options:
    - Global:
    - Miner:
        - Text files miner:
            - Text files: paths of the texts of the corpus to mine.
            - Database: path to the database where the n-grams will be stored.
            - n: maximum n-grams size.
            - Lowercase: weither the texts words should be lowered or not.
        - Facebook miner:
            - Access Token: token authorizing the program to access the
                profile.
            - Database: path to the database where the n-grams will be stored.
            - n: maximum n-grams size.
            - Lowercase: weither the texts words should be lowered or not.
        - Twitter miner:
    - Predictor:
        - Corpus n-gram:
            - Database: path to the database from which n-grams will be
                retrieved.
            - n: maximum n-grams size to retrieved from the database.
            - Deltas: weight of the n-gram in function of its position.
        - Input n-gram:
            - Database: path to the database from which n-grams will be
                retrieved.
            - n: maximum n-grams size to retrieved from the database.
            - Deltas: weight of the n-gram in function of its position.
        - Facebook n-gram:
            - Database: path to the database from which n-grams will be
                retrieved.
            - n: maximum n-grams size to retrieved from the database.
            - Deltas: weight of the n-gram in function of its position.
        - Last occur:
            - Lambda
            - N0
            - Cuttoff threshold
        - Memorize:
            - Memory: path of the file where the tokens are stored.
            - Trigger
    - Merger:
    - Merger: name of the merging method to use.
    - Selector:
        - Number of suggestions: number of suggested words to display.
        - Greedy suggestions threshold: don't display words appearing less
            than it.
    - PredictorActivator:
    - stoplist: path of the file containing undesired words (one per line).
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
from tipy.lg import lg


probabilistic_Merger = 0
ALPHABETICAL_Merger = 1


class Settings_UI(QtWidgets.QDialog):
    def __init__(self, config, parent=None):
        super(Settings_UI, self).__init__(parent)
        self.config = config
        self.setupUi()
        self.read_config()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.cwd = path.dirname(path.realpath(__file__))

    def setupUi(self):
        ########################## LAYOUTS TO BE USED ##########################
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout_25 = QtWidgets.QGridLayout()
        self.gridLayout_27 = QtWidgets.QGridLayout()
        self.gridLayout_36 = QtWidgets.QGridLayout()
        self.gridLayout_39 = QtWidgets.QGridLayout()
        self.gridLayout_34 = QtWidgets.QGridLayout()
        self.gridLayout_35 = QtWidgets.QGridLayout()
        self.FBGRID = QtWidgets.QGridLayout()
        self.gridLayout_32 = QtWidgets.QGridLayout()
        self.gridLayout_40 = QtWidgets.QGridLayout()
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_19 = QtWidgets.QGridLayout()
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_20 = QtWidgets.QGridLayout()
        self.gridLayout_21 = QtWidgets.QGridLayout()
        ########################## THE SETTINGS DIALOG #########################
        self.resize(691, 484)
        self.setWindowTitle("Settings")
        self.gridLayout_3 = QtWidgets.QGridLayout(self)
        # Sections tab widget
        self.tabWidgetSections = QtWidgets.QTabWidget(self)
        ############################## GLOBAL TAB ##############################
        self.tab = QtWidgets.QWidget()
        # Add the Global tab to the sections tab widget
        self.tabWidgetSections.addTab(self.tab, "Global")
        ############################## MINERS TAB ##############################
        self.tabMiner = QtWidgets.QWidget()
        self.gridLayout_43 = QtWidgets.QGridLayout(self.tabMiner)
        # ===================== MINERS SELECTION GROUP BOX =================== #
        self.groupBoxMiners = QtWidgets.QGroupBox(self.tabMiner)
        self.groupBoxMiners.setTitle("Miner type")
        self.gridLayout_26 = QtWidgets.QGridLayout(self.groupBoxMiners)
        # Miner selection label
        self.labelMinerSelection = QtWidgets.QLabel(self.groupBoxMiners)
        self.labelMinerSelection.setText(
            'Please select the miner(s) to use for text mining (you can '
            'choose multiple miners):')
        # CorpusMiner checkbox
        self.checkBoxCorpMiner = QtWidgets.QCheckBox(self.groupBoxMiners)
        self.checkBoxCorpMiner.setText("Corpus")
        # FbMiner checkbox
        self.checkBoxFbMiner = QtWidgets.QCheckBox(self.groupBoxMiners)
        self.checkBoxFbMiner.setText("Facebook")
        # TwitterMiner checkbox
        self.checkBoxTwitMiner = QtWidgets.QCheckBox(self.groupBoxMiners)
        self.checkBoxTwitMiner.setText("Twitter")
        # ===================== MINERS SETTINGS GROUP BOX ==================== #
        self.groupBoxMinersSettings = QtWidgets.QGroupBox(self.tabMiner)
        self.groupBoxMinersSettings.setTitle("Miner\'s settings")
        self.gridLayout_28 = QtWidgets.QGridLayout(self.groupBoxMinersSettings)
        # Miners tab widget
        self.tabWidgetMiners = QtWidgets.QTabWidget(
            self.groupBoxMinersSettings)
        #-------------------------- CORPUS MINER TAB --------------------------#
        self.tabCorpMiner = QtWidgets.QWidget()
        self.gridLayout_29 = QtWidgets.QGridLayout(self.tabCorpMiner)
        # CorpusMiner files label
        self.labelCorpMinerFiles = QtWidgets.QLabel(self.tabCorpMiner)
        self.labelCorpMinerFiles.setText("Text files:")
        self.listCorpMinerFiles = QtWidgets.QListWidget(self.tabCorpMiner)
        self.verticalLayout_2.addWidget(self.listCorpMinerFiles)
        # Add text file push button
        self.pushButtonCorpMinerAddFile = QtWidgets.QPushButton(
            self.tabCorpMiner)
        self.pushButtonCorpMinerAddFile.setText("Add")
        self.pushButtonCorpMinerAddFile.released.connect(
            self.on_add_file_btn_released)
        self.horizontalLayout_3.addWidget(self.pushButtonCorpMinerAddFile)
        # Remove text file push button
        self.pushButtonCorpMinerRmFile = QtWidgets.QPushButton(
            self.tabCorpMiner)
        self.pushButtonCorpMinerRmFile.setText("Remove")
        self.pushButtonCorpMinerRmFile.released.connect(
            self.on_rm_file_btn_released)
        self.horizontalLayout_3.addWidget(self.pushButtonCorpMinerRmFile)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        # CorpusMiner database label
        self.labelCorpMinerDb = QtWidgets.QLabel(self.tabCorpMiner)
        self.labelCorpMinersetText("Database:")
        self.toolButtonCorpMiner = QtWidgets.QToolButton(self.tabCorpMiner)
        # CorpusMiner database toolbutton
        self.toolButtonCorpMiner.setText("...")
        self.toolButtonCorpMiner.released.connect(
            self.on_corp_miner_db_tool_button_released)
        # CorpusMiner database lineedit
        self.lineEditCorpMinerDb = QtWidgets.QLineEdit(self.tabCorpMiner)
        # CorpusMiner n label
        self.LabelCorpMinerN = QtWidgets.QLabel(self.tabCorpMiner)
        self.LabelCorpMinerN.setText("N-gram size:")
        self.spinBoxCorpMinerN = QtWidgets.QSpinBox(self.tabCorpMiner)
        self.spinBoxCorpMinerN.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        # CorpusMiner lowercase mode label
        self.labelCorpMinerLower = QtWidgets.QLabel(self.tabCorpMiner)
        self.labelCorpMinerLower.setText("Lowercase mode:")
        self.checkBoxCorpMinerLower = QtWidgets.QCheckBox(self.tabCorpMiner)
        self.checkBoxCorpMinerLower.setText('Lowercase:')
        # Add the Corpus tab to the miners tab widget
        self.tabWidgetMiners.addTab(self.tabCorpMiner, "Corpus")
        #------------------------- FACEBOOK MINER TAB -------------------------#
        self.tabMinerFb = QtWidgets.QWidget()
        self.gridLayout_33 = QtWidgets.QGridLayout(self.tabMinerFb)
        # FbMiner access token label
        self.labelFbMinerAccessToken = QtWidgets.QLabel(self.tabMinerFb)
        self.labelFbMinerAccessToken.setText("Access Token:")
        # FbMiner access token lineedit
        self.lineEditFbMinerAccessToken = QtWidgets.QLineEdit(self.tabMinerFb)
        # FbMiner database label
        self.LabelFbMinerDb = QtWidgets.QLabel(self.tabMinerFb)
        self.LabelFbMinersetText("Database:")
        # FbMiner satabase toolbutton
        self.toolButtonFbMiner = QtWidgets.QToolButton(self.tabMinerFb)
        self.toolButtonFbMiner.setText("...")
        self.toolButtonFbMiner.released.connect(
            self.on_fb_miner_db_tool_button_released)
        # FbMiner database lineedit
        self.lineEditFbMinerDb = QtWidgets.QLineEdit(self.tabMinerFb)
        # FbMiner n label
        self.LabelFbMinerN = QtWidgets.QLabel(self.tabMinerFb)
        self.LabelFbMinerN.setText("N-gram size:")
        self.spinBoxFbMinerN = QtWidgets.QSpinBox(self.tabMinerFb)
        self.spinBoxFbMinerN.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        # FbMiner loxercase mode label
        self.labelFbMinerLower = QtWidgets.QLabel(self.tabMinerFb)
        self.labelFbMinerLower.setText("Lowercase mode:")
        self.checkBoxFbMinerLower = QtWidgets.QCheckBox(self.tabMinerFb)
        # Add the Facebook tab to the miners tab widget
        self.tabWidgetMiners.addTab(self.tabMinerFb, "Facebook")
        #------------------------- TWITTER MINER TAB --------------------------#
        self.tabMinerTwit = QtWidgets.QWidget()
        self.gridLayout_37 = QtWidgets.QGridLayout(self.tabMinerTwit)
        # Twitter not implemented label
        self.labelTwitMinerSettings = QtWidgets.QLabel(self.tabMinerTwit)
        self.labelTwitMinerSettings.setText("[NOT IMPLEMENTED YET]")
        self.labelTwitMinerSettings.setAlignment(QtCore.Qt.AlignCenter)
        # Add the Twitter tab to the miners tab widget
        self.tabWidgetMiners.addTab(self.tabMinerTwit, "Twitter")
        # Add the Miner tab to the sections tab widget
        self.tabWidgetSections.addTab(self.tabMiner, "Miner")
        ############################ PREDICTORS TAB ############################
        self.tabPredictor = QtWidgets.QWidget()
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabPredictor)
        # ================== PREDICTORS SELECTION GROUP BOX ================== #
        self.groupBoxPreds = QtWidgets.QGroupBox(self.tabPredictor)
        self.groupBoxPreds.setTitle("Predictor type")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBoxPreds)
        # Predictor selection label
        self.label = QtWidgets.QLabel(self.groupBoxPreds)
        self.label.setText("Please select the predictor(s) to use for word "
                           "suggestion (you can choose multiple predictors):")
        self.checkBoxLateOccurPred = QtWidgets.QCheckBox(self.groupBoxPreds)
        self.checkBoxLateOccurPred.setText("Late Occur")
        self.checkBoxCorpNgramPred = QtWidgets.QCheckBox(self.groupBoxPreds)
        self.checkBoxCorpNgramPred.setText("Corpus n-gram")
        self.checkBoxInpNgramPred = QtWidgets.QCheckBox(self.groupBoxPreds)
        self.checkBoxInpNgramPred.setText("Input n-gram")
        self.checkBoxFbNgramPred = QtWidgets.QCheckBox(self.groupBoxPreds)
        self.checkBoxFbNgramPred.setText("Facebook n-gram")
        self.checkBoxMemorizePred = QtWidgets.QCheckBox(self.groupBoxPreds)
        self.checkBoxMemorizePred.setText("Memorize")
        # =================== PREDICTORS SETTINGS GROUP BOX ================== #
        self.groupBoxPredSettings = QtWidgets.QGroupBox(self.tabPredictor)
        self.groupBoxPredSettings.setTitle("Predictor\'s settings")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBoxPredSettings)
        self.tabWidgetPreds = QtWidgets.QTabWidget(self.groupBoxPredSettings)
        #--------------------- CORPUS NGRAM PREDICTOR TAB ---------------------#
        self.tabCorpNgramPred = QtWidgets.QWidget()
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tabCorpNgramPred)
        # CorpusNgramPredictor database label
        self.labelCorpNgramPredDb = QtWidgets.QLabel(self.tabCorpNgramPred)
        self.labelCorpNgramPredsetText("Database file:")
        # CorpusNgramPredictor database lineedit
        self.lineEditCorpNgramPredDb = QtWidgets.QLineEdit(
            self.tabCorpNgramPred)
        # CorpusNgramPredictor database toolbutton
        self.toolButtonCorpNgramPredDb = QtWidgets.QToolButton(
            self.tabCorpNgramPred)
        self.toolButtonCorpNgramPredsetText("...")
        self.toolButtonCorpNgramPredreleased.connect(
            self.on_corp_ngram_pred_db_tool_button_released)
        # CorpusNgramPredictor n label
        self.labelCorpNgramPredN = QtWidgets.QLabel(self.tabCorpNgramPred)
        self.labelCorpNgramPredN.setText("N-gram size:")
        # CorpusNgramPredictor n spinbox
        self.spinBoxCorpNgramPredN = QtWidgets.QSpinBox(self.tabCorpNgramPred)
        self.spinBoxCorpNgramPredN.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBoxCorpNgramPredN.setMinimum(1)
        self.spinBoxCorpNgramPredN.setMaximum(8)
        # CorpusNgramPredictor deltas label
        self.labelCorpNgramPredDeltas = QtWidgets.QLabel(self.tabCorpNgramPred)
        self.labelCorpNgramPredDeltas.setText("Deltas:")
        # CorpusNgramPredictor deltas doublespinboxes
        self.doubleSpinBoxCorpNgramPredDelta1 = QtWidgets.QDoubleSpinBox(
            self.tabCorpNgramPred)
        self.doubleSpinBoxCorpNgramPredDelta1.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxCorpNgramPredDelta2 = QtWidgets.QDoubleSpinBox(
            self.tabCorpNgramPred)
        self.doubleSpinBoxCorpNgramPredDelta2.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxCorpNgramPredDelta3 = QtWidgets.QDoubleSpinBox(
            self.tabCorpNgramPred)
        self.doubleSpinBoxCorpNgramPredDelta3.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxCorpNgramPredDelta4 = QtWidgets.QDoubleSpinBox(
            self.tabCorpNgramPred)
        self.doubleSpinBoxCorpNgramPredDelta4.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxCorpNgramPredDelta5 = QtWidgets.QDoubleSpinBox(
            self.tabCorpNgramPred)
        self.doubleSpinBoxCorpNgramPredDelta5.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxCorpNgramPredDelta6 = QtWidgets.QDoubleSpinBox(
            self.tabCorpNgramPred)
        self.doubleSpinBoxCorpNgramPredDelta6.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxCorpNgramPredDelta7 = QtWidgets.QDoubleSpinBox(
            self.tabCorpNgramPred)
        self.doubleSpinBoxCorpNgramPredDelta7.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxCorpNgramPredDelta8 = QtWidgets.QDoubleSpinBox(
            self.tabCorpNgramPred)
        self.doubleSpinBoxCorpNgramPredDelta8.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        # Add the Corpus n-gram tab to the predictors tab widget
        self.tabWidgetPreds.addTab(self.tabCorpNgramPred, "Corpus n-gram")
        #---------------------- INPUT NGRAM PREDICTOR TAB ---------------------#
        self.tabInpNgramPred = QtWidgets.QWidget()
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tabInpNgramPred)
        # InputNgramPredictor database label
        self.labelInpNgramPredDb = QtWidgets.QLabel(self.tabInpNgramPred)
        self.labelInpNgramPredsetText("Database file:")
        # InputNgramPredictor database lineedit
        self.lineEditInpNgramPredDb = QtWidgets.QLineEdit(self.tabInpNgramPred)
        # InputNgramPredictor database toolbutton
        self.toolButtonInpNgramPredDb = QtWidgets.QToolButton(
            self.tabInpNgramPred)
        self.toolButtonInpNgramPredsetText("...")
        self.toolButtonInpNgramPredreleased.connect(
            self.on_inp_ngram_pred_db_tool_button_released)
        # InputNgramPredictor n label
        self.labelInpNgramPredN = QtWidgets.QLabel(self.tabInpNgramPred)
        self.labelInpNgramPredN.setText("N-gram size:")
        # InputNgramPredictor n spinbox
        self.spinBoxInpNgramPredN = QtWidgets.QSpinBox(self.tabInpNgramPred)
        self.spinBoxInpNgramPredN.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBoxInpNgramPredN.setMinimum(1)
        self.spinBoxInpNgramPredN.setMaximum(8)
        # InputNgramPredictor deltas label
        self.labelInpNgramPredDeltas = QtWidgets.QLabel(self.tabInpNgramPred)
        self.labelInpNgramPredDeltas.setText("Deltas:")
        # InputNgramPredictor deltas doublespinboxes
        self.doubleSpinBoxInpNgramPredDelta1 = QtWidgets.QDoubleSpinBox(
            self.tabInpNgramPred)
        self.doubleSpinBoxInpNgramPredDelta1.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxInpNgramPredDelta2 = QtWidgets.QDoubleSpinBox(
            self.tabInpNgramPred)
        self.doubleSpinBoxInpNgramPredDelta2.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxInpNgramPredDelta3 = QtWidgets.QDoubleSpinBox(
            self.tabInpNgramPred)
        self.doubleSpinBoxInpNgramPredDelta3.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxInpNgramPredDelta4 = QtWidgets.QDoubleSpinBox(
            self.tabInpNgramPred)
        self.doubleSpinBoxInpNgramPredDelta4.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxInpNgramPredDelta5 = QtWidgets.QDoubleSpinBox(
            self.tabInpNgramPred)
        self.doubleSpinBoxInpNgramPredDelta5.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxInpNgramPredDelta6 = QtWidgets.QDoubleSpinBox(
            self.tabInpNgramPred)
        self.doubleSpinBoxInpNgramPredDelta6.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxInpNgramPredDelta7 = QtWidgets.QDoubleSpinBox(
            self.tabInpNgramPred)
        self.doubleSpinBoxInpNgramPredDelta7.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxInpNgramPredDelta8 = QtWidgets.QDoubleSpinBox(
            self.tabInpNgramPred)
        self.doubleSpinBoxInpNgramPredDelta8.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        # Add the Input n-gram tab to the predictors tab widget
        self.tabWidgetPreds.addTab(self.tabInpNgramPred, "Input n-gram")
        #-------------------- FACEBOOK NGRAM PREDICTOR TAB --------------------#
        self.tabFbNgramPred = QtWidgets.QWidget()
        self.gridLayout_41 = QtWidgets.QGridLayout(self.tabFbNgramPred)
        # InputNgramPredictor database label
        self.labelFbNgramPredDb = QtWidgets.QLabel(self.tabFbNgramPred)
        self.labelFbNgramPredsetText("Database file:")
        # InputNgramPredictor database lineedit
        self.lineEditFbNgramPredDb = QtWidgets.QLineEdit(self.tabFbNgramPred)
        # InputNgramPredictor database toolbutton
        self.toolButtonFbNgramPredDb = QtWidgets.QToolButton(
            self.tabFbNgramPred)
        self.toolButtonFbNgramPredsetText("...")
        self.toolButtonFbNgramPredreleased.connect(
            self.on_fb_ngram_pred_db_tool_button_released)
        # InputNgramPredictor n label
        self.labelFbNgramPredN = QtWidgets.QLabel(self.tabFbNgramPred)
        self.labelFbNgramPredN.setText("N-gram size:")
        # InputNgramPredictor n spinbox
        self.spinBoxFbNgramPredN = QtWidgets.QSpinBox(self.tabFbNgramPred)
        self.spinBoxFbNgramPredN.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBoxFbNgramPredN.setMinimum(1)
        self.spinBoxFbNgramPredN.setMaximum(8)
        # InputNgramPredictor deltas label
        self.labelFbNgramPredDeltas = QtWidgets.QLabel(self.tabFbNgramPred)
        self.labelFbNgramPredDeltas.setText("Deltas:")
        # InputNgramPredictor deltas doublespinboxes
        self.doubleSpinBoxFbNgramPredDelta6 = QtWidgets.QDoubleSpinBox(
            self.tabFbNgramPred)
        self.doubleSpinBoxFbNgramPredDelta6.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxFbNgramPredDelta2 = QtWidgets.QDoubleSpinBox(
            self.tabFbNgramPred)
        self.doubleSpinBoxFbNgramPredDelta2.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxFbNgramPredDelta1 = QtWidgets.QDoubleSpinBox(
            self.tabFbNgramPred)
        self.doubleSpinBoxFbNgramPredDelta1.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxFbNgramPredDelta5 = QtWidgets.QDoubleSpinBox(
            self.tabFbNgramPred)
        self.doubleSpinBoxFbNgramPredDelta5.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxFbNgramPredDelta3 = QtWidgets.QDoubleSpinBox(
            self.tabFbNgramPred)
        self.doubleSpinBoxFbNgramPredDelta3.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxFbNgramPredDelta4 = QtWidgets.QDoubleSpinBox(
            self.tabFbNgramPred)
        self.doubleSpinBoxFbNgramPredDelta4.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxFbNgramPredDelta7 = QtWidgets.QDoubleSpinBox(
            self.tabFbNgramPred)
        self.doubleSpinBoxFbNgramPredDelta7.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.doubleSpinBoxFbNgramPredDelta8 = QtWidgets.QDoubleSpinBox(
            self.tabFbNgramPred)
        self.doubleSpinBoxFbNgramPredDelta8.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.tabWidgetPreds.addTab(self.tabFbNgramPred, 'Facebook n-gram')
        #---------------------- LATE OCCUR PREDICTOR TAB ----------------------#
        self.tabLateOccurPred = QtWidgets.QWidget()
        self.gridLayout_15 = QtWidgets.QGridLayout(self.tabLateOccurPred)
        self.gridLayout_14.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        # LateOccurPredictor cutoff threshold label
        self.labelLateOccurPredCutoff = QtWidgets.QLabel(self.tabLateOccurPred)
        self.labelLateOccurPredCutoff.setText("Cutoff threshold:")
        # LateOccurPredictor cutoff threshold spinbox
        self.spinBoxLateOccurPredCutoff = QtWidgets.QSpinBox(
            self.tabLateOccurPred)
        self.spinBoxLateOccurPredCutoff.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        # LateOccurPredictor N0 label
        self.labelLateOccurPredN0 = QtWidgets.QLabel(self.tabLateOccurPred)
        self.labelLateOccurPredN0.setText("N0:")
        # LateOccurPredictor N0 spinbox
        self.spinBoxLateOccurPredN0 = QtWidgets.QSpinBox(self.tabLateOccurPred)
        self.spinBoxLateOccurPredN0.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBoxLateOccurPredN0.setMinimum(0)
        # LateOccurPredictor lambda label
        self.labelLateOccurPredLambda = QtWidgets.QLabel(self.tabLateOccurPred)
        self.labelLateOccurPredLambda.setText("Lambda:")
        self.spinBoxLateOccurPredLambda = QtWidgets.QSpinBox(
            self.tabLateOccurPred)
        self.spinBoxLateOccurPredLambda.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.spinBoxLateOccurPredLambda.setMinimum(0)
        # Add Late occur tab to the predictors tab widget
        self.tabWidgetPreds.addTab(self.tabLateOccurPred, "Late occur")
        #----------------------- MEMORIZE PREDICTOR TAB -----------------------#
        self.tabMemorizePred = QtWidgets.QWidget()
        self.gridLayout_17 = QtWidgets.QGridLayout(self.tabMemorizePred)
        # MemorizePredictor memory label
        self.labelMemorizePredMemory = QtWidgets.QLabel(self.tabMemorizePred)
        self.labelMemorizePredMemory.setText("Memory file:")
        # MemorizePredictor memory lineedit
        self.lineEditMemorizePredMemory = QtWidgets.QLineEdit(
            self.tabMemorizePred)
        # MemorizePredictor memory toolbutton
        self.toolButtonMemorizePredMemory = QtWidgets.QToolButton(
            self.tabMemorizePred)
        self.toolButtonMemorizePredMemory.setText("...")
        self.toolButtonMemorizePredMemory.released.connect(
            self.on_dejavu_pred_memory_tool_button_released)
        # MemorizePredictor trigger label
        self.labelMemorizePredTrigger = QtWidgets.QLabel(self.tabMemorizePred)
        self.labelMemorizePredTrigger.setText("Trigger:")
        # MemorizePredictor trigger spinbox
        self.spinBoxMemorizePredTrigger = QtWidgets.QSpinBox(
            self.tabMemorizePred)
        self.spinBoxMemorizePredTrigger.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        # Add the Memorize tab to the predictors tab widget
        self.tabWidgetPreds.addTab(self.tabMemorizePred, "Memorize")
        # Add Predictor tab to the sections tab widget
        self.tabWidgetSections.addTab(self.tabPredictor, "Predictor")
        ############################# Merger TAB #############################
        self.tabMerger = QtWidgets.QWidget()
        self.gridLayout_38 = QtWidgets.QGridLayout(self.tabMerger)
        # ==================== Merger SELECTION GROUP BOX ================== #
        self.groupBoxMerger = QtWidgets.QGroupBox(self.tabMerger)
        self.groupBoxMerger.setTitle("Merger type")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.groupBoxMerger)
        # Merger selection label
        self.labelSelectMerger = QtWidgets.QLabel(self.groupBoxMerger)
        self.labelSelectMerger.setText("Please select the Merger to use:")
        # Merger selection combobox
        self.comboBoxMergers = QtWidgets.QComboBox(self.groupBoxMerger)
        self.comboBoxMergers.addItem("probabilistic")
        self.comboBoxMergers.addItem("Alphabetical")
        # Add  theMerger tab to the sections tab widget
        self.tabWidgetSections.addTab(self.tabMerger, "Merger")
        ############################# SELECTOR TAB #############################
        self.tabSelector = QtWidgets.QWidget()
        self.gridLayout_24 = QtWidgets.QGridLayout(self.tabSelector)
        # ==================== SELECTOR SETTINGS GROUP BOX =================== #
        self.groupBoxSelector = QtWidgets.QGroupBox(self.tabSelector)
        self.groupBoxSelector.setTitle("Selector\'s settings")
        self.gridLayout_23 = QtWidgets.QGridLayout(self.groupBoxSelector)
        # Selector greedy suggestions threshold label
        self.labelSelectorGreedy = QtWidgets.QLabel(self.groupBoxSelector)
        self.labelSelectorGreedy.setText("Greedy suggestions threshold:")
        # Selector greedy suggestions threshold spinbox
        self.spinBoxSelectorGreedy = QtWidgets.QSpinBox(self.groupBoxSelector)
        self.spinBoxSelectorGreedy.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        # Selector suggestions number label
        self.labelSelectorSuggestions = QtWidgets.QLabel(self.groupBoxSelector)
        self.labelSelectorSuggestions.setText("Number of suggestions:")
        # Selector suggestions number spinbox
        self.spinBoxSelectorSuggestions = QtWidgets.QSpinBox(
            self.groupBoxSelector)
        self.spinBoxSelectorSuggestions.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        # Add the Selector tab to the sections tab widget
        self.tabWidgetSections.addTab(self.tabSelector, "Selector")
        ############################# STOPLIST TAB #############################
        self.tabStopList = QtWidgets.QWidget()
        self.gridLayout_30 = QtWidgets.QGridLayout(self.tabStopList)
        # Stoplist selection label
        self.labelSelectStoplist = QtWidgets.QLabel(self.tabStopList)
        self.labelSelectStoplist.setText("Please add the stoplists to use:")
        self.verticalLayout.addWidget(self.labelSelectStoplist)
        # Stoplist list
        self.listStoplists = QtWidgets.QListWidget(self.tabStopList)
        self.verticalLayout.addWidget(self.listStoplists)
        # Add stoplist file pushbutton
        self.pushButtonAddStoplist = QtWidgets.QPushButton(self.tabStopList)
        self.pushButtonAddStoplist.setText("Add")
        self.pushButtonAddStoplist.released.connect(
            self.on_add_stoplist_btn_released)
        self.horizontalLayout.addWidget(self.pushButtonAddStoplist)
        # Remove stoplist file pushbutton
        self.pushButtonRmStoplist = QtWidgets.QPushButton(self.tabStopList)
        self.pushButtonRmStoplist.setText("Remove")
        self.pushButtonRmStoplist.released.connect(
            self.on_rm_stoplist_btn_released)
        self.horizontalLayout.addWidget(self.pushButtonRmStoplist)
        self.verticalLayout.addLayout(self.horizontalLayout)
        # Add the Stoplist tab to the sections tab widget
        self.tabWidgetSections.addTab(self.tabStopList, "Stoplist")
        ###################### ADD EVERYTHING TO LAYOUTS #######################
        self.gridLayout_26.addWidget(self.labelMinerSelection, 0, 0, 1, 1)
        self.gridLayout_27.addWidget(self.checkBoxCorpMiner, 0, 0, 1, 1)
        self.gridLayout_27.addWidget(self.checkBoxFbMiner, 0, 1, 1, 1)
        self.gridLayout_27.addWidget(self.checkBoxTwitMiner, 1, 0, 1, 1)
        self.gridLayout_26.addLayout(self.gridLayout_27, 1, 0, 1, 1)
        self.gridLayout_25.addWidget(self.groupBoxMiners, 0, 0, 1, 1)
        self.gridLayout_36.addWidget(self.labelCorpMinerFiles, 0, 0, 1, 1)
        self.gridLayout_36.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.gridLayout_36.addWidget(self.labelCorpMinerDb, 1, 0, 1, 1)
        self.gridLayout_36.addWidget(self.LabelCorpMinerN, 2, 0, 1, 1)
        self.gridLayout_36.addWidget(self.spinBoxCorpMinerN, 2, 1, 1, 1)
        self.gridLayout_39.addWidget(self.lineEditCorpMinerDb, 0, 0, 1, 1)
        self.gridLayout_39.addWidget(self.toolButtonCorpMiner, 0, 1, 1, 1)
        self.gridLayout_36.addLayout(self.gridLayout_39, 1, 1, 1, 1)
        self.gridLayout_36.addWidget(self.labelCorpMinerLower, 3, 0, 1, 1)
        self.gridLayout_36.addWidget(self.checkBoxCorpMinerLower, 3, 1, 1, 1)
        self.gridLayout_29.addLayout(self.gridLayout_36, 0, 0, 1, 1)
        self.gridLayout_34.addWidget(self.LabelFbMinerN, 2, 0, 1, 1)
        self.gridLayout_34.addWidget(
            self.lineEditFbMinerAccessToken, 0, 1, 1, 1)
        self.gridLayout_34.addWidget(self.LabelFbMinerDb, 1, 0, 1, 1)
        self.gridLayout_34.addWidget(self.labelFbMinerAccessToken, 0, 0, 1, 1)
        self.gridLayout_34.addWidget(self.spinBoxFbMinerN, 2, 1, 1, 1)
        self.gridLayout_35.addWidget(self.lineEditFbMinerDb, 0, 0, 1, 1)
        self.gridLayout_35.addWidget(self.toolButtonFbMiner, 0, 1, 1, 1)
        self.gridLayout_34.addLayout(self.gridLayout_35, 1, 1, 1, 1)
        self.gridLayout_34.addWidget(self.labelFbMinerLower, 3, 0, 1, 1)
        self.gridLayout_34.addWidget(self.checkBoxFbMinerLower, 3, 1, 1, 1)
        self.gridLayout_33.addLayout(self.gridLayout_34, 0, 0, 1, 1)
        self.gridLayout_37.addWidget(self.labelTwitMinerSettings, 0, 0, 1, 1)
        self.gridLayout_28.addWidget(self.tabWidgetMiners, 0, 0, 1, 1)
        self.gridLayout_25.addWidget(self.groupBoxMinersSettings, 1, 0, 1, 1)
        self.gridLayout_43.addLayout(self.gridLayout_25, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.checkBoxCorpNgramPred, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.checkBoxInpNgramPred, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.checkBoxFbNgramPred, 1, 0, 1, 1)
        self.gridLayout_7.addWidget(self.checkBoxMemorizePred, 1, 1, 1, 1)
        self.gridLayout_7.addWidget(self.checkBoxLateOccurPred, 2, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_7, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxPreds, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.spinBoxCorpNgramPredN, 1, 1, 1, 1)
        self.gridLayout_18.addWidget(self.toolButtonCorpNgramPredDb, 0, 1, 1, 1)
        self.gridLayout_18.addWidget(self.lineEditCorpNgramPredDb, 0, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_18, 0, 1, 1, 1)
        self.gridLayout_8.addWidget(self.labelCorpNgramPredDeltas, 2, 0, 1, 1)
        self.gridLayout_8.addWidget(self.labelCorpNgramPredN, 1, 0, 1, 1)
        self.gridLayout_8.addWidget(self.labelCorpNgramPredDb, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(
            self.doubleSpinBoxCorpNgramPredDelta8, 1, 1, 1, 1)
        self.gridLayout_9.addWidget(
            self.doubleSpinBoxCorpNgramPredDelta2, 0, 1, 1, 1)
        self.gridLayout_9.addWidget(
            self.doubleSpinBoxCorpNgramPredDelta1, 0, 0, 1, 1)
        self.gridLayout_9.addWidget(
            self.doubleSpinBoxCorpNgramPredDelta6, 1, 0, 1, 1)
        self.gridLayout_9.addWidget(
            self.doubleSpinBoxCorpNgramPredDelta3, 0, 2, 1, 1)
        self.gridLayout_9.addWidget(
            self.doubleSpinBoxCorpNgramPredDelta4, 0, 3, 1, 1)
        self.gridLayout_9.addWidget(
            self.doubleSpinBoxCorpNgramPredDelta5, 1, 2, 1, 1)
        self.gridLayout_9.addWidget(
            self.doubleSpinBoxCorpNgramPredDelta7, 1, 3, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_9, 2, 1, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.gridLayout_11.addWidget(self.labelInpNgramPredDb, 0, 0, 1, 1)
        self.gridLayout_11.addWidget(self.labelInpNgramPredN, 1, 0, 1, 1)
        self.gridLayout_11.addWidget(self.spinBoxInpNgramPredN, 1, 1, 1, 1)
        self.gridLayout_11.addWidget(self.labelInpNgramPredDeltas, 2, 0, 1, 1)
        self.gridLayout_12.addWidget(
            self.doubleSpinBoxInpNgramPredDelta6, 1, 1, 1, 1)
        self.gridLayout_12.addWidget(
            self.doubleSpinBoxInpNgramPredDelta2, 0, 1, 1, 1)
        self.gridLayout_12.addWidget(
            self.doubleSpinBoxInpNgramPredDelta1, 0, 0, 1, 1)
        self.gridLayout_12.addWidget(
            self.doubleSpinBoxInpNgramPredDelta5, 1, 0, 1, 1)
        self.gridLayout_12.addWidget(
            self.doubleSpinBoxInpNgramPredDelta3, 0, 2, 1, 1)
        self.gridLayout_12.addWidget(
            self.doubleSpinBoxInpNgramPredDelta4, 0, 3, 1, 1)
        self.gridLayout_12.addWidget(
            self.doubleSpinBoxInpNgramPredDelta7, 1, 2, 1, 1)
        self.gridLayout_12.addWidget(
            self.doubleSpinBoxInpNgramPredDelta8, 1, 3, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_12, 2, 1, 1, 1)
        self.gridLayout_19.addWidget(self.toolButtonInpNgramPredDb, 0, 1, 1, 1)
        self.gridLayout_19.addWidget(self.lineEditInpNgramPredDb, 0, 0, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_19, 0, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_11, 0, 0, 1, 1)
        self.FBGRID.addWidget(self.labelFbNgramPredDb, 0, 0, 1, 1)
        self.FBGRID.addWidget(self.labelFbNgramPredN, 1, 0, 1, 1)
        self.FBGRID.addWidget(self.spinBoxFbNgramPredN, 1, 1, 1, 1)
        self.FBGRID.addWidget(self.labelFbNgramPredDeltas, 2, 0, 1, 1)
        self.gridLayout_32.addWidget(
            self.doubleSpinBoxFbNgramPredDelta6, 1, 1, 1, 1)
        self.gridLayout_32.addWidget(
            self.doubleSpinBoxFbNgramPredDelta2, 0, 1, 1, 1)
        self.gridLayout_32.addWidget(
            self.doubleSpinBoxFbNgramPredDelta1, 0, 0, 1, 1)
        self.gridLayout_32.addWidget(
            self.doubleSpinBoxFbNgramPredDelta5, 1, 0, 1, 1)
        self.gridLayout_32.addWidget(
            self.doubleSpinBoxFbNgramPredDelta3, 0, 2, 1, 1)
        self.gridLayout_32.addWidget(
            self.doubleSpinBoxFbNgramPredDelta4, 0, 3, 1, 1)
        self.gridLayout_32.addWidget(
            self.doubleSpinBoxFbNgramPredDelta7, 1, 2, 1, 1)
        self.gridLayout_32.addWidget(
            self.doubleSpinBoxFbNgramPredDelta8, 1, 3, 1, 1)
        self.FBGRID.addLayout(self.gridLayout_32, 2, 1, 1, 1)
        self.gridLayout_40.addWidget(self.toolButtonFbNgramPredDb, 0, 1, 1, 1)
        self.gridLayout_40.addWidget(self.lineEditFbNgramPredDb, 0, 0, 1, 1)
        self.FBGRID.addLayout(self.gridLayout_40, 0, 1, 1, 1)
        self.gridLayout_41.addLayout(self.FBGRID, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.labelLateOccurPredCutoff, 2, 0, 1, 1)
        self.gridLayout_14.addWidget(self.labelLateOccurPredN0, 1, 0, 1, 1)
        self.gridLayout_14.addWidget(self.labelLateOccurPredLambda, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(
            self.spinBoxLateOccurPredLambda, 0, 1, 1, 1)
        self.gridLayout_14.addWidget(self.spinBoxLateOccurPredN0, 1, 1, 1, 1)
        self.gridLayout_14.addWidget(
            self.spinBoxLateOccurPredCutoff, 2, 1, 1, 1)
        self.gridLayout_15.addLayout(self.gridLayout_14, 0, 0, 1, 1)
        self.gridLayout_16.addWidget(self.labelMemorizePredMemory, 0, 0, 1, 1)
        self.gridLayout_16.addWidget(self.labelMemorizePredTrigger, 1, 0, 1, 1)
        self.gridLayout_16.addWidget(
            self.spinBoxMemorizePredTrigger, 1, 1, 1, 1)
        self.gridLayout_20.addWidget(
            self.toolButtonMemorizePredMemory, 0, 1, 1, 1)
        self.gridLayout_20.addWidget(
            self.lineEditMemorizePredMemory, 0, 0, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_20, 0, 1, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_16, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.tabWidgetPreds, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxPredSettings, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_22.addWidget(self.labelSelectMerger, 0, 0, 1, 1)
        self.gridLayout_22.addWidget(self.comboBoxMergers, 1, 0, 1, 1)
        self.gridLayout_21.addWidget(self.groupBoxMerger, 0, 0, 1, 1)
        self.gridLayout_38.addLayout(self.gridLayout_21, 0, 0, 1, 1)
        self.gridLayout_23.addWidget(self.labelSelectorGreedy, 1, 0, 1, 1)
        self.gridLayout_23.addWidget(self.labelSelectorSuggestions, 0, 0, 1, 1)
        self.gridLayout_23.addWidget(
            self.spinBoxSelectorSuggestions, 0, 1, 1, 1)
        self.gridLayout_23.addWidget(self.spinBoxSelectorGreedy, 1, 1, 1, 1)
        self.gridLayout_24.addWidget(self.groupBoxSelector, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.tabWidgetSections, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_30.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.tabWidgetSections, 0, 0, 1, 1)

    def read_config(self):
        # settings that can be modified by the settings dialog:
        # Global:
        # Miner:
        #     Miners
        miners = self.config.getas('MinerRegistry', 'miners', 'list')
        self.checkBoxCorpMiner.setChecked('CorpusMiner' in miners)
        self.checkBoxFbMiner.setChecked('FbMiner' in miners)
        self.checkBoxTwitMiner.setChecked('TwitterMiner' in miners)
        #     Text files miner:
        #         Text files
        self.listCorpMinerFiles.clear()
        files = self.config.getas('CorpusMiner', 'texts', 'list')
        for f in files:
            self.listCorpMinerFiles.addItem(f)
        #         Database
        database = self.config.getas('CorpusMiner', 'database')
        self.lineEditCorpMinersetText(database)
        #         n
        n = self.config.getas('CorpusMiner', 'n', 'int')
        self.spinBoxCorpMinerN.setValue(n)
        #         Lowercase
        lower = self.config.getas('CorpusMiner', 'lowercase', 'bool')
        self.checkBoxCorpMinerLower.setChecked(lower)
        #     Facebook miner:
        #         Access Token
        accessToken = self.config.getas('FbMiner', 'accesstoken')
        self.lineEditFbMinerAccessToken.setText(accessToken)
        #         Database
        database = self.config.getas('FbMiner', 'database')
        self.lineEditFbMinersetText(database)
        #         n
        n = self.config.getas('FbMiner', 'n', 'int')
        self.spinBoxFbMinerN.setValue(n)
        #         Lowercase
        lower = self.config.getas('FbMiner', 'lowercase', 'bool')
        self.checkBoxFbMinerLower.setChecked(lower)
        #     Twitter miner:
        # Predictor:
        #     Predictors
        preds = self.config.getas('PredictorRegistry', 'predictors', 'list')
        self.checkBoxCorpNgramPred.setChecked('CorpusNgramPredictor' in preds)
        self.checkBoxInpNgramPred.setChecked('InputNgramPredictor' in preds)
        self.checkBoxFbNgramPred.setChecked('FbNgramPredictor' in preds)
        self.checkBoxLateOccurPred.setChecked('LateOccurPredictor' in preds)
        self.checkBoxMemorizePred.setChecked('MemorizePredictor' in preds)
        #     Corpus n-gram:
        #         Database
        database = self.config.getas('CorpusNgramPredictor', 'database')
        self.lineEditCorpNgramPredsetText(database)
        #         n
        deltas = self.config.getas(
            'CorpusNgramPredictor', 'deltas', 'floatlist')
        self.spinBoxCorpNgramPredN.setValue(len(deltas))
        #         Deltas
        boxes = [self.doubleSpinBoxCorpNgramPredDelta1,
                 self.doubleSpinBoxCorpNgramPredDelta2,
                 self.doubleSpinBoxCorpNgramPredDelta3,
                 self.doubleSpinBoxCorpNgramPredDelta4,
                 self.doubleSpinBoxCorpNgramPredDelta5,
                 self.doubleSpinBoxCorpNgramPredDelta6,
                 self.doubleSpinBoxCorpNgramPredDelta7,
                 self.doubleSpinBoxCorpNgramPredDelta8]
        for i, delta in enumerate(deltas):
            boxes[i].setValue(delta)
        for i in range(len(deltas) + 1, len(boxes)):
            boxes[i].setValue(0)
            boxes[i].setEnabled(False)
        #     Input n-gram:
        #         Database
        database = self.config.getas('InputNgramPredictor', 'database')
        self.lineEditInpNgramPredsetText(database)
        #         n
        deltas = self.config.getas('InputNgramPredictor', 'deltas', 'floatlist')
        self.spinBoxInpNgramPredN.setValue(len(deltas))
        #         Deltas
        boxes = [self.doubleSpinBoxInpNgramPredDelta1,
                 self.doubleSpinBoxInpNgramPredDelta2,
                 self.doubleSpinBoxInpNgramPredDelta3,
                 self.doubleSpinBoxInpNgramPredDelta4,
                 self.doubleSpinBoxInpNgramPredDelta5,
                 self.doubleSpinBoxInpNgramPredDelta6,
                 self.doubleSpinBoxInpNgramPredDelta7,
                 self.doubleSpinBoxInpNgramPredDelta8]
        for i, delta in enumerate(deltas):
            boxes[i].setValue(delta)
        for i in range(len(deltas) + 1, len(boxes)):
            boxes[i].setValue(0)
            boxes[i].setEnabled(False)
        #     Facebook n-gram:
        #         Database
        database = self.config.getas('FbNgramPredictor', 'database')
        self.lineEditFbNgramPredsetText(database)
        #         n
        deltas = self.config.getas('FbNgramPredictor', 'deltas', 'floatlist')
        self.spinBoxFbNgramPredN.setValue(len(deltas))
        #         Deltas
        boxes = [self.doubleSpinBoxFbNgramPredDelta1,
                 self.doubleSpinBoxFbNgramPredDelta2,
                 self.doubleSpinBoxFbNgramPredDelta3,
                 self.doubleSpinBoxFbNgramPredDelta4,
                 self.doubleSpinBoxFbNgramPredDelta5,
                 self.doubleSpinBoxFbNgramPredDelta6,
                 self.doubleSpinBoxFbNgramPredDelta7,
                 self.doubleSpinBoxFbNgramPredDelta8]
        for i, delta in enumerate(deltas):
            boxes[i].setValue(delta)
        for i in range(len(deltas) + 1, len(boxes)):
            boxes[i].setValue(0)
            boxes[i].setEnabled(False)
        #     Last occur:
        #         Lambda
        lambdar = self.config.getas('LateOccurPredictor', 'lambda', 'int')
        self.spinBoxLateOccurPredLambda.setValue(lambdar)
        #         N0
        n0 = self.config.getas('LateOccurPredictor', 'n_0', 'int')
        self.spinBoxLateOccurPredN0.setValue(n0)
        #         Cuttoff threshold
        cutoff = self.config.getas(
            'LateOccurPredictor', 'cutoff_threshold', 'int')
        self.spinBoxLateOccurPredCutoff.setValue(cutoff)
        #     Memorize:
        #         Memory
        memory = self.config.getas('MemorizePredictor', 'memory')
        self.lineEditMemorizePredMemory.setText(memory)
        #         Trigger
        trigger = self.config.getas('MemorizePredictor', 'trigger', 'int')
        self.spinBoxMemorizePredTrigger.setValue(trigger)
        # Merger:
        #     Merger
        Merger = self.config.getas(
            'PredictorActivator', 'merging_method').lower()
        if Merger == 'probabilistic':
            self.comboBoxMergers.setCurrentIndex(probabilistic_Merger)
        elif Merger == 'alphabetical':
            self.comboBoxMergers.setCurrentIndex(ALPHABETICAL_Merger)
        # Selector:
        #     Number of suggestions
        noSuggestions = self.config.getas('Selector', 'suggestions', 'int')
        self.spinBoxSelectorSuggestions.setValue(noSuggestions)
        #     Greedy suggestions threshold
        greedyTreshold = self.config.getas(
            'Selector', 'greedy_suggestion_threshold', 'int')
        self.spinBoxSelectorGreedy.setValue(greedyTreshold)
        # PredictorActivator:
        #     stoplist
        self.listStoplists.clear()
        stoplists = self.config.getas('PredictorActivator', 'stoplist', 'list')
        for sl in stoplists:
            self.listStoplists.addItem(sl)

    def closeEvent(self, event):
        self.save_config()
        event.accept()

    def done(self, code):
        self.save_config()

    def save_config(self):
        # settings that can be modified by the settings dialog:
        # Global:
        # Miner:
        #     Miners
        self.config['MinerRegistry']['MINERS'] = ''
        if self.checkBoxCorpMiner.isChecked():
            self.config['MinerRegistry']['MINERS'] += 'CorpusMiner '
        if self.checkBoxFbMiner.isChecked():
            self.config['MinerRegistry']['MINERS'] += 'FbMiner '
        if self.checkBoxTwitMiner.isChecked():
            self.config['MinerRegistry']['MINERS'] += 'TwitterMiner '
        #     Text files miner:
        #         Text files
        self.config['CorpusMiner']['TEXTS'] = ''
        for index in range(self.listCorpMinerFiles.count()):
            self.config['CorpusMiner']['TEXTS'] += \
                self.listCorpMinerFiles.item(index).text() + ' '
        #         Database
        self.config['CorpusMiner']['database'] = \
            self.lineEditCorpMinertext()
        #         n
        self.config['CorpusMiner']['n'] = \
            str(self.spinBoxCorpMinerN.value())
        #         Lowercase
        if self.checkBoxCorpMinerLower.isChecked():
            self.config['CorpusMiner']['lowercase'] = 'True'
        else:
            self.config['CorpusMiner']['lowercase'] = 'False'
        #     Facebook miner:
        #         Access Token
        self.config['FbMiner']['ACCESSTOKEN'] = \
            self.lineEditFbMinerAccessToken.text()
        #         Database
        self.config['FbMiner']['database'] = self.lineEditFbMinertext()
        #         n
        self.config['FbMiner']['n'] = \
            str(self.spinBoxFbMinerN.value())
        #         Lowercase
        if self.checkBoxFbMinerLower.isChecked():
            self.config['FbMiner']['lowercase'] = 'True'
        else:
            self.config['FbMiner']['lowercase'] = 'False'
        #     Twitter miner:
        # Predictor:
        #     Predictors
        self.config['PredictorRegistry']['PREDICTORS'] = ''
        if self.checkBoxCorpNgramPred.isChecked():
            self.config['PredictorRegistry']['PREDICTORS'] += \
                'CorpusNgramPredictor '
        if self.checkBoxInpNgramPred.isChecked():
            self.config['PredictorRegistry']['PREDICTORS'] += \
                'InputNgramPredictor '
        if self.checkBoxFbNgramPred.isChecked():
            self.config['PredictorRegistry']['PREDICTORS'] += \
                'FbNgramPredictor '
        if self.checkBoxLateOccurPred.isChecked():
            self.config['PredictorRegistry']['PREDICTORS'] += \
                'LateOccurPredictor '
        if self.checkBoxMemorizePred.isChecked():
            self.config['PredictorRegistry']['PREDICTORS'] += \
                'MemorizePredictor '
        #     Corpus n-gram:
        #         Database
        self.config['CorpusNgramPredictor']['database'] = \
            self.lineEditCorpNgramPredtext()
        #         Deltas
        self.config['CorpusNgramPredictor']['DELTAS'] = ''
        boxes = [self.doubleSpinBoxCorpNgramPredDelta1,
                 self.doubleSpinBoxCorpNgramPredDelta2,
                 self.doubleSpinBoxCorpNgramPredDelta3,
                 self.doubleSpinBoxCorpNgramPredDelta4,
                 self.doubleSpinBoxCorpNgramPredDelta5,
                 self.doubleSpinBoxCorpNgramPredDelta6,
                 self.doubleSpinBoxCorpNgramPredDelta7,
                 self.doubleSpinBoxCorpNgramPredDelta8]
        for box in boxes:
            if box.isEnabled() and box.value() != 0:
                self.config['CorpusNgramPredictor']['DELTAS'] += \
                    str(box.value()) + ' '
        #     Input n-gram:
        #         Database
        self.config['InputNgramPredictor']['database'] = \
            self.lineEditInpNgramPredtext()
        #         n
        deltas = self.config['InputNgramPredictor']['DELTAS'].split()
        self.spinBoxInpNgramPredN.setValue(len(deltas))
        #         Deltas
        self.config['InputNgramPredictor']['DELTAS'] = ''
        boxes = [self.doubleSpinBoxInpNgramPredDelta1,
                 self.doubleSpinBoxInpNgramPredDelta2,
                 self.doubleSpinBoxInpNgramPredDelta3,
                 self.doubleSpinBoxInpNgramPredDelta4,
                 self.doubleSpinBoxInpNgramPredDelta5,
                 self.doubleSpinBoxInpNgramPredDelta6,
                 self.doubleSpinBoxInpNgramPredDelta7,
                 self.doubleSpinBoxInpNgramPredDelta8]
        for box in boxes:
            if box.isEnabled() and box.value() != 0:
                self.config['InputNgramPredictor']['DELTAS'] += \
                    str(box.value()) + ' '
        #     Facebook n-gram:
        #         Database
        self.config['FbNgramPredictor']['database'] = \
            self.lineEditFbNgramPredtext()
        #         n
        deltas = self.config['FbNgramPredictor']['DELTAS'].split()
        self.spinBoxFbNgramPredN.setValue(len(deltas))
        #         Deltas
        self.config['FbNgramPredictor']['DELTAS'] = ''
        boxes = [self.doubleSpinBoxFbNgramPredDelta1,
                 self.doubleSpinBoxFbNgramPredDelta2,
                 self.doubleSpinBoxFbNgramPredDelta3,
                 self.doubleSpinBoxFbNgramPredDelta4,
                 self.doubleSpinBoxFbNgramPredDelta5,
                 self.doubleSpinBoxFbNgramPredDelta6,
                 self.doubleSpinBoxFbNgramPredDelta7,
                 self.doubleSpinBoxFbNgramPredDelta8]
        for box in boxes:
            if box.isEnabled() and box.value() != 0:
                self.config['FbNgramPredictor']['DELTAS'] += \
                    str(box.value()) + ' '
        #     Last occur:
        #         Lambda
        self.config['LateOccurPredictor']['LAMBDA'] = \
            str(self.spinBoxLateOccurPredLambda.value())
        #         N0
        self.config['LateOccurPredictor']['N_0'] = \
            str(self.spinBoxLateOccurPredN0.value())
        #         Cuttoff threshold
        self.config['LateOccurPredictor']['CUTOFF_THRESHOLD'] = \
            str(self.spinBoxLateOccurPredCutoff.value())
        #     Memorize:
        #         Memory
        self.config['MemorizePredictor']['MEMORY'] = \
            self.lineEditMemorizePredMemory.text()
        #         Trigger
        self.config['MemorizePredictor']['TRIGGER'] = \
            str(self.spinBoxMemorizePredTrigger.value())
        # Merger:
        #     Merger
        self.config['PredictorActivator']['merging_method'] = \
            self.comboBoxMergers.currentText()
        # Selector:
        #     Number of suggestions
        self.config['Selector']['SUGGESTIONS'] = \
            str(self.spinBoxSelectorSuggestions.value())
        #     Greedy suggestions threshold
        self.config['Selector']['GREEDY_SUGGESTION_THRESHOLD'] = \
            str(self.spinBoxSelectorGreedy.value())
        lg.info('Configuration file saved.')

    def shorten_path(self, path):
        if path.startswith(self.cwd):
            return path.replace(self.cwd, '.')
        return path

    def on_add_file_btn_released(self):
        cwd = path.dirname(path.realpath(__file__))
        fName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open text file", cwd)
        if fName[0]:
            self.listCorpMinerFiles.addItem(self.shorten_path(fName[0]))

    def on_rm_file_btn_released(self):
        listItems = self.listCorpMinerFiles.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.listCorpMinerFiles.takeItem(self.listCorpMinerFiles.row(item))

    def on_add_stoplist_btn_released(self):
        cwd = path.dirname(path.realpath(__file__))
        fName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open text file", cwd)
        if fName[0]:
            self.listStoplists.addItem(self.shorten_path(fName[0]))

    def on_rm_stoplist_btn_released(self):
        listItems = self.listStoplists.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.listStoplists.takeItem(self.listStoplists.row(item))

    def on_corp_miner_db_tool_button_released(self):
        fName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open database file", self.cwd,
            "SQLite database (*.db *.sqlite)")
        if fName[0]:
            self.lineEditCorpMinersetText(self.shorten_path(fName[0]))

    def on_fb_miner_db_tool_button_released(self):
        fName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open database file", self.cwd,
            "SQLite database (*.db *.sqlite)")
        if fName[0]:
            self.lineEditFbMinersetText(self.shorten_path(fName[0]))

    def on_corp_ngram_pred_db_tool_button_released(self):
        fName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open database file", self.cwd,
            "SQLite database (*.db *.sqlite)")
        if fName[0]:
            self.lineEditCorpNgramPredsetText(self.shorten_path(fName[0]))

    def on_inp_ngram_pred_db_tool_button_released(self):
        fName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open database file", self.cwd,
            "SQLite database (*.db *.sqlite)")
        if fName[0]:
            self.lineEditInpNgramPredsetText(self.shorten_path(fName[0]))

    def on_fb_ngram_pred_db_tool_button_released(self):
        fName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open database file", self.cwd,
            "SQLite database (*.db *.sqlite)")
        if fName[0]:
            self.lineEditFbNgramPredsetText(self.shorten_path(fName[0]))

    def on_dejavu_pred_memory_tool_button_released(self):
        fName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open text file", self.cwd, "Text (*.txt)")
        if fName[0]:
            self.lineEditMemorizePredMemory.setText(
                self.shorten_path(fName[0]))
