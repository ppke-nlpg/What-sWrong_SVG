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
        ChooseFormat.resize(393, 274)
        self.radioButton2000 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton2000.setGeometry(QtCore.QRect(9, 9, 113, 22))
        self.radioButton2000.setObjectName("radioButton2000")
        self.radioButton_MalTab = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_MalTab.setGeometry(QtCore.QRect(128, 9, 81, 22))
        self.radioButton_MalTab.setObjectName("radioButton_MalTab")
        self.radioButton_2002 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2002.setGeometry(QtCore.QRect(9, 37, 113, 22))
        self.radioButton_2002.setObjectName("radioButton_2002")
        self.radioButton_gale = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_gale.setGeometry(QtCore.QRect(128, 37, 189, 22))
        self.radioButton_gale.setObjectName("radioButton_gale")
        self.radioButton_2003 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2003.setGeometry(QtCore.QRect(9, 65, 113, 22))
        self.radioButton_2003.setObjectName("radioButton_2003")
        self.radioButton_giza = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_giza.setGeometry(QtCore.QRect(128, 65, 188, 22))
        self.radioButton_giza.setObjectName("radioButton_giza")
        self.radioButton_2004 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2004.setGeometry(QtCore.QRect(9, 93, 113, 22))
        self.radioButton_2004.setObjectName("radioButton_2004")
        self.radioButton_the_beast = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_the_beast.setGeometry(QtCore.QRect(128, 93, 152, 22))
        self.radioButton_the_beast.setObjectName("radioButton_the_beast")
        self.radioButton_2005 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2005.setGeometry(QtCore.QRect(9, 121, 113, 22))
        self.radioButton_2005.setObjectName("radioButton_2005")
        self.radioButton_lisp_s_expr = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_lisp_s_expr.setGeometry(QtCore.QRect(128, 121, 158, 22))
        self.radioButton_lisp_s_expr.setObjectName("radioButton_lisp_s_expr")
        self.radioButton_2006 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2006.setGeometry(QtCore.QRect(9, 149, 113, 22))
        self.radioButton_2006.setObjectName("radioButton_2006")
        self.radioButton_bionlp_2009 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_bionlp_2009.setGeometry(QtCore.QRect(128, 149, 252, 22))
        self.radioButton_bionlp_2009.setObjectName("radioButton_bionlp_2009")
        self.radioButton_2008 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2008.setGeometry(QtCore.QRect(9, 177, 113, 22))
        self.radioButton_2008.setObjectName("radioButton_2008")
        self.radioButton_2009 = QtWidgets.QRadioButton(ChooseFormat)
        self.radioButton_2009.setGeometry(QtCore.QRect(9, 205, 113, 22))
        self.radioButton_2009.setObjectName("radioButton_2009")
        self.buttonBox = QtWidgets.QDialogButtonBox(ChooseFormat)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setGeometry(QtCore.QRect(200, 233, 176, 27))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(ChooseFormat)
        self.buttonBox.accepted.connect(ChooseFormat.accept)
        self.buttonBox.rejected.connect(ChooseFormat.reject)
        QtCore.QMetaObject.connectSlotsByName(ChooseFormat)

    def retranslateUi(self, ChooseFormat):
        _translate = QtCore.QCoreApplication.translate
        ChooseFormat.setWindowTitle(_translate("ChooseFormat", "Choose format"))
        self.radioButton2000.setText(_translate("ChooseFormat", "CoNLL 2000"))
        self.radioButton_MalTab.setText(_translate("ChooseFormat", "MalTab"))
        self.radioButton_2002.setText(_translate("ChooseFormat", "CoNLL 2002"))
        self.radioButton_gale.setText(_translate("ChooseFormat", "Gale Alignment Format"))
        self.radioButton_2003.setText(_translate("ChooseFormat", "CoNLL 2003"))
        self.radioButton_giza.setText(_translate("ChooseFormat", "Giza Alignment Format"))
        self.radioButton_2004.setText(_translate("ChooseFormat", "CoNLL 2004"))
        self.radioButton_the_beast.setText(_translate("ChooseFormat", "The Beast Format"))
        self.radioButton_2005.setText(_translate("ChooseFormat", "CoNLL 2005"))
        self.radioButton_lisp_s_expr.setText(_translate("ChooseFormat", "Lisp S-expr Format"))
        self.radioButton_2006.setText(_translate("ChooseFormat", "CoNLL 2006"))
        self.radioButton_bionlp_2009.setText(_translate("ChooseFormat", "BioNLP2009 Shared Task Format"))
        self.radioButton_2008.setText(_translate("ChooseFormat", "CoNLL 2008"))
        self.radioButton_2009.setText(_translate("ChooseFormat", "CoNLL 2009"))

