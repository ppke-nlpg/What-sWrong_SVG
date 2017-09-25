# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chooseFormat.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChooseFormat(object):
    def setupUi(self, ChooseFormat):
        ChooseFormat.setObjectName("ChooseFormat")
        ChooseFormat.resize(474, 357)
        self.radioButton2000 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton2000.setGeometry(QtCore.QRect(10, 21, 111, 20))
        self.radioButton2000.setObjectName("radioButton2000")
        self.buttonBox = QtWidgets.QDialogButtonBox(ChooseFormat)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setGeometry(QtCore.QRect(6, 304, 164, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.radioButton_MalTab = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_MalTab.setGeometry(QtCore.QRect(10, 261, 111, 20))
        self.radioButton_MalTab.setObjectName("radioButton_MalTab")
        self.radioButton_2009 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2009.setGeometry(QtCore.QRect(10, 231, 111, 20))
        self.radioButton_2009.setObjectName("radioButton_2009")
        self.radioButton_2008 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2008.setGeometry(QtCore.QRect(10, 201, 111, 20))
        self.radioButton_2008.setObjectName("radioButton_2008")
        self.radioButton_2006 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2006.setGeometry(QtCore.QRect(10, 171, 111, 20))
        self.radioButton_2006.setObjectName("radioButton_2006")
        self.radioButton_2005 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2005.setGeometry(QtCore.QRect(10, 141, 111, 20))
        self.radioButton_2005.setObjectName("radioButton_2005")
        self.radioButton_2004 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2004.setGeometry(QtCore.QRect(10, 111, 111, 20))
        self.radioButton_2004.setObjectName("radioButton_2004")
        self.radioButton_2003 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2003.setGeometry(QtCore.QRect(10, 81, 111, 20))
        self.radioButton_2003.setObjectName("radioButton_2003")
        self.radioButton_2002 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2002.setGeometry(QtCore.QRect(10, 51, 111, 20))
        self.radioButton_2002.setObjectName("radioButton_2002")

        self.retranslateUi(ChooseFormat)
        self.buttonBox.accepted.connect(ChooseFormat.accept)
        self.buttonBox.rejected.connect(ChooseFormat.reject)
        QtCore.QMetaObject.connectSlotsByName(ChooseFormat)

    def retranslateUi(self, ChooseFormat):
        _translate = QtCore.QCoreApplication.translate
        ChooseFormat.setWindowTitle(_translate("ChooseFormat", "Choose format"))
        self.radioButton2000.setText(_translate("ChooseFormat", "CoNLL 2000"))
        self.radioButton_MalTab.setText(_translate("ChooseFormat", "MalTab"))
        self.radioButton_2009.setText(_translate("ChooseFormat", "CoNLL 2009"))
        self.radioButton_2008.setText(_translate("ChooseFormat", "CoNLL 2008"))
        self.radioButton_2006.setText(_translate("ChooseFormat", "CoNLL 2006"))
        self.radioButton_2005.setText(_translate("ChooseFormat", "CoNLL 2005"))
        self.radioButton_2004.setText(_translate("ChooseFormat", "CoNLL 2004"))
        self.radioButton_2003.setText(_translate("ChooseFormat", "CoNLL 2003"))
        self.radioButton_2002.setText(_translate("ChooseFormat", "CoNLL 2002"))

