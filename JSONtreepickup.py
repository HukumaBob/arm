# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JSONtreepickup.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_json(object):
    def setupUi(self, Dialog_json):
        Dialog_json.setObjectName("Dialog_json")
        Dialog_json.resize(753, 75)
        Dialog_json.setMinimumSize(QtCore.QSize(700, 0))
        self.gridLayout = QtWidgets.QGridLayout(Dialog_json)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonAdd = QtWidgets.QPushButton(Dialog_json)
        self.pushButtonAdd.setMaximumSize(QtCore.QSize(23, 16777215))
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout.addWidget(self.pushButtonAdd, 1, 0, 1, 1)
        self.lineEditMain1 = QtWidgets.QLineEdit(Dialog_json)
        self.lineEditMain1.setMinimumSize(QtCore.QSize(500, 0))
        self.lineEditMain1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lineEditMain1.setObjectName("lineEditMain1")
        self.gridLayout.addWidget(self.lineEditMain1, 1, 2, 1, 1)
        self.lineEditAttribute = QtWidgets.QLineEdit(Dialog_json)
        self.lineEditAttribute.setObjectName("lineEditAttribute")
        self.gridLayout.addWidget(self.lineEditAttribute, 0, 0, 1, 3)
        self.lineEditKey1 = QtWidgets.QLineEdit(Dialog_json)
        self.lineEditKey1.setMinimumSize(QtCore.QSize(120, 0))
        self.lineEditKey1.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEditKey1.setObjectName("lineEditKey1")
        self.gridLayout.addWidget(self.lineEditKey1, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog_json)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 3, 1, 1)
        self.pushButtonDelete = QtWidgets.QPushButton(Dialog_json)
        self.pushButtonDelete.setMaximumSize(QtCore.QSize(23, 16777215))
        self.pushButtonDelete.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.gridLayout.addWidget(self.pushButtonDelete, 1, 3, 1, 1)

        self.retranslateUi(Dialog_json)
        QtCore.QMetaObject.connectSlotsByName(Dialog_json)

    def retranslateUi(self, Dialog_json):
        _translate = QtCore.QCoreApplication.translate
        Dialog_json.setWindowTitle(_translate("Dialog_json", "Dialog"))
        self.pushButtonAdd.setText(_translate("Dialog_json", "+"))
        self.lineEditMain1.setPlaceholderText(_translate("Dialog_json", "Main text 1"))
        self.lineEditAttribute.setPlaceholderText(_translate("Dialog_json", "Attribute"))
        self.lineEditKey1.setPlaceholderText(_translate("Dialog_json", "Key1"))
        self.pushButton.setText(_translate("Dialog_json", "Save"))
        self.pushButtonDelete.setText(_translate("Dialog_json", "-"))

