# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(767, 628)
        MainWindow.setMinimumSize(QtCore.QSize(767, 628))
        MainWindow.setSizeIncrement(QtCore.QSize(1, 1))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(0, 225))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 741, 223))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents_2)
        self.graphicsView.setEnabled(True)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_8.addWidget(self.scrollArea_2, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 741, 294))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.selectGuessListWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.selectGuessListWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.selectGuessListWidget.setObjectName("selectGuessListWidget")
        self.verticalLayout_3.addWidget(self.selectGuessListWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addGuessPushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.addGuessPushButton.setObjectName("addGuessPushButton")
        self.horizontalLayout.addWidget(self.addGuessPushButton)
        self.removeGuessPushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.removeGuessPushButton.setObjectName("removeGuessPushButton")
        self.horizontalLayout.addWidget(self.removeGuessPushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.selectGoldListWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.selectGoldListWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.selectGoldListWidget.setProperty("isWrapping", False)
        self.selectGoldListWidget.setObjectName("selectGoldListWidget")
        self.verticalLayout_2.addWidget(self.selectGoldListWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButtonAddGold = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonAddGold.setObjectName("pushButtonAddGold")
        self.horizontalLayout_2.addWidget(self.pushButtonAddGold)
        self.removeGoldPushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.removeGoldPushButton.setObjectName("removeGoldPushButton")
        self.horizontalLayout_2.addWidget(self.removeGoldPushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 1, 1, 1)
        self.searchCorpusTab = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.searchCorpusTab.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.searchCorpusTab.setObjectName("searchCorpusTab")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.collapsCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.collapsCheckBox.setObjectName("collapsCheckBox")
        self.gridLayout_6.addWidget(self.collapsCheckBox, 12, 1, 1, 1)
        self.EdgeLabelLabel = QtWidgets.QLabel(self.tab_2)
        self.EdgeLabelLabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.EdgeLabelLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EdgeLabelLabel.setObjectName("EdgeLabelLabel")
        self.gridLayout_6.addWidget(self.EdgeLabelLabel, 8, 0, 1, 1)
        self.onlyPathCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.onlyPathCheckBox.setObjectName("onlyPathCheckBox")
        self.gridLayout_6.addWidget(self.onlyPathCheckBox, 11, 1, 1, 1)
        self.EdgeFilterTokenLabel = QtWidgets.QLabel(self.tab_2)
        self.EdgeFilterTokenLabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.EdgeFilterTokenLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EdgeFilterTokenLabel.setObjectName("EdgeFilterTokenLabel")
        self.gridLayout_6.addWidget(self.EdgeFilterTokenLabel, 10, 0, 1, 1)
        self.edgeFilterTokenLineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.edgeFilterTokenLineEdit.setObjectName("edgeFilterTokenLineEdit")
        self.gridLayout_6.addWidget(self.edgeFilterTokenLineEdit, 10, 1, 1, 1)
        self.edgeFilterWholeWordsCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.edgeFilterWholeWordsCheckBox.setObjectName("edgeFilterWholeWordsCheckBox")
        self.gridLayout_6.addWidget(self.edgeFilterWholeWordsCheckBox, 13, 1, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.edgeTypeListWidget = QtWidgets.QListWidget(self.tab_2)
        self.edgeTypeListWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.edgeTypeListWidget.setObjectName("edgeTypeListWidget")
        self.horizontalLayout_5.addWidget(self.edgeTypeListWidget)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.matchesCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.matchesCheckBox.setObjectName("matchesCheckBox")
        self.verticalLayout_5.addWidget(self.matchesCheckBox)
        self.falsePositiveCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.falsePositiveCheckBox.setObjectName("falsePositiveCheckBox")
        self.verticalLayout_5.addWidget(self.falsePositiveCheckBox)
        self.falseNegativeCheckBox = QtWidgets.QCheckBox(self.tab_2)
        self.falseNegativeCheckBox.setObjectName("falseNegativeCheckBox")
        self.verticalLayout_5.addWidget(self.falseNegativeCheckBox)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.gridLayout_6.addLayout(self.horizontalLayout_5, 1, 0, 1, 2)
        self.EdgeFilterOptionsLabel = QtWidgets.QLabel(self.tab_2)
        self.EdgeFilterOptionsLabel.setObjectName("EdgeFilterOptionsLabel")
        self.gridLayout_6.addWidget(self.EdgeFilterOptionsLabel, 11, 0, 1, 1)
        self.labelLineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.labelLineEdit.setObjectName("labelLineEdit")
        self.gridLayout_6.addWidget(self.labelLineEdit, 8, 1, 1, 1)
        self.searchCorpusTab.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tokenFilterWholeWordsCheckBox = QtWidgets.QCheckBox(self.tab_3)
        self.tokenFilterWholeWordsCheckBox.setObjectName("tokenFilterWholeWordsCheckBox")
        self.gridLayout_3.addWidget(self.tokenFilterWholeWordsCheckBox, 4, 1, 1, 1)
        self.TokenFilterOptionsLabel = QtWidgets.QLabel(self.tab_3)
        self.TokenFilterOptionsLabel.setObjectName("TokenFilterOptionsLabel")
        self.gridLayout_3.addWidget(self.TokenFilterOptionsLabel, 3, 1, 1, 1)
        self.tokenTypesListWidget = QtWidgets.QListWidget(self.tab_3)
        self.tokenTypesListWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tokenTypesListWidget.setObjectName("tokenTypesListWidget")
        self.gridLayout_3.addWidget(self.tokenTypesListWidget, 1, 0, 6, 1)
        self.ShowPropertiesLabel = QtWidgets.QLabel(self.tab_3)
        self.ShowPropertiesLabel.setObjectName("ShowPropertiesLabel")
        self.gridLayout_3.addWidget(self.ShowPropertiesLabel, 0, 0, 1, 1)
        self.TokenFiltersTokenLabel = QtWidgets.QLabel(self.tab_3)
        self.TokenFiltersTokenLabel.setObjectName("TokenFiltersTokenLabel")
        self.gridLayout_3.addWidget(self.TokenFiltersTokenLabel, 0, 1, 1, 1)
        self.tokenFilterTokenLineEdit = QtWidgets.QLineEdit(self.tab_3)
        self.tokenFilterTokenLineEdit.setObjectName("tokenFilterTokenLineEdit")
        self.gridLayout_3.addWidget(self.tokenFilterTokenLineEdit, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 2, 1, 1, 1)
        self.searchCorpusTab.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.searchCorpusLineEdit = QtWidgets.QLineEdit(self.tab_5)
        self.searchCorpusLineEdit.setObjectName("searchCorpusLineEdit")
        self.gridLayout_4.addWidget(self.searchCorpusLineEdit, 0, 0, 1, 1)
        self.searchButton = QtWidgets.QPushButton(self.tab_5)
        self.searchButton.setObjectName("searchButton")
        self.gridLayout_4.addWidget(self.searchButton, 0, 1, 1, 1)
        self.searchResultLisWidget = QtWidgets.QListWidget(self.tab_5)
        self.searchResultLisWidget.setObjectName("searchResultLisWidget")
        self.gridLayout_4.addWidget(self.searchResultLisWidget, 1, 0, 1, 2)
        self.searchCorpusTab.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.searchCorpusTab, 3, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_8.addWidget(self.scrollArea, 6, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_10.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spinBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spinBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_10.addWidget(self.spinBox)
        self.SpinBoxLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SpinBoxLabel.sizePolicy().hasHeightForWidth())
        self.SpinBoxLabel.setSizePolicy(sizePolicy)
        self.SpinBoxLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpinBoxLabel.setIndent(-1)
        self.SpinBoxLabel.setObjectName("SpinBoxLabel")
        self.horizontalLayout_10.addWidget(self.SpinBoxLabel)
        self.gridLayout_8.addLayout(self.horizontalLayout_10, 5, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 767, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImprt = QtWidgets.QAction(MainWindow)
        self.actionImprt.setObjectName("actionImprt")
        self.actionAddGold = QtWidgets.QAction(MainWindow)
        self.actionAddGold.setCheckable(True)
        self.actionAddGold.setObjectName("actionAddGold")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.menuFile.addAction(self.actionExport)
        self.menubar.addAction(self.menuFile.menuAction())
        self.SpinBoxLabel.setBuddy(self.spinBox)

        self.retranslateUi(MainWindow)
        self.searchCorpusTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "What's Wrong With My NLP?"))
        self.label_2.setText(_translate("MainWindow", "Select Guess"))
        self.addGuessPushButton.setText(_translate("MainWindow", "Add"))
        self.removeGuessPushButton.setText(_translate("MainWindow", "Remove"))
        self.label.setText(_translate("MainWindow", "Select Gold"))
        self.pushButtonAddGold.setText(_translate("MainWindow", "Add"))
        self.removeGoldPushButton.setText(_translate("MainWindow", "Remove"))
        self.collapsCheckBox.setText(_translate("MainWindow", "Collaps"))
        self.EdgeLabelLabel.setText(_translate("MainWindow", "Label:"))
        self.onlyPathCheckBox.setText(_translate("MainWindow", "Only Path"))
        self.EdgeFilterTokenLabel.setText(_translate("MainWindow", "Token:"))
        self.edgeFilterWholeWordsCheckBox.setText(_translate("MainWindow", "Whole Words"))
        self.matchesCheckBox.setText(_translate("MainWindow", "Matches"))
        self.falsePositiveCheckBox.setText(_translate("MainWindow", "False Positive"))
        self.falseNegativeCheckBox.setText(_translate("MainWindow", "False Negative"))
        self.EdgeFilterOptionsLabel.setText(_translate("MainWindow", "Options:"))
        self.searchCorpusTab.setTabText(self.searchCorpusTab.indexOf(self.tab_2), _translate("MainWindow", "Edge Filter"))
        self.tokenFilterWholeWordsCheckBox.setText(_translate("MainWindow", "Whole Words"))
        self.TokenFilterOptionsLabel.setText(_translate("MainWindow", "Options:"))
        self.ShowPropertiesLabel.setText(_translate("MainWindow", "Show Properties"))
        self.TokenFiltersTokenLabel.setText(_translate("MainWindow", "Token:"))
        self.searchCorpusTab.setTabText(self.searchCorpusTab.indexOf(self.tab_3), _translate("MainWindow", "Token Filters"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.searchCorpusTab.setTabText(self.searchCorpusTab.indexOf(self.tab_5), _translate("MainWindow", "Search Corpus"))
        self.SpinBoxLabel.setText(_translate("MainWindow", "of 0"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionImprt.setText(_translate("MainWindow", "Imprt"))
        self.actionAddGold.setText(_translate("MainWindow", "AddGold"))
        self.actionAddGold.setToolTip(_translate("MainWindow", "Add Gold File"))
        self.actionExport.setText(_translate("MainWindow", "Export"))

