# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JSONeditor.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 1020)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 516, 880))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_manipulation = QtWidgets.QComboBox(self.frame)
        self.comboBox_manipulation.setMaxVisibleItems(50)
        self.comboBox_manipulation.setObjectName("comboBox_manipulation")
        self.horizontalLayout.addWidget(self.comboBox_manipulation)
        self.comboBox_anatomical_part = QtWidgets.QComboBox(self.frame)
        self.comboBox_anatomical_part.setObjectName("comboBox_anatomical_part")
        self.horizontalLayout.addWidget(self.comboBox_anatomical_part)
        self.verticalLayout_2.addWidget(self.frame)
        self.comboBox_ds = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_ds.setObjectName("comboBox_ds")
        self.verticalLayout_2.addWidget(self.comboBox_ds)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeWidgetDS = QtWidgets.QTreeWidget(self.scrollAreaWidgetContents)
        self.treeWidgetDS.setObjectName("treeWidgetDS")
        self.verticalLayout_3.addWidget(self.treeWidgetDS)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 516, 880))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textEditDS = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        self.textEditDS.setObjectName("textEditDS")
        self.horizontalLayout_3.addWidget(self.textEditDS)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_2.addWidget(self.scrollArea_2)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.general_frame = QtWidgets.QFrame(self.centralwidget)
        self.general_frame.setMinimumSize(QtCore.QSize(0, 20))
        self.general_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.general_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.general_frame.setObjectName("general_frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.general_frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_one = QtWidgets.QFrame(self.general_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_one.sizePolicy().hasHeightForWidth())
        self.frame_one.setSizePolicy(sizePolicy)
        self.frame_one.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_one.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_one.setObjectName("frame_one")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_one)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_6.addWidget(self.frame_one, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.gridLayout.addWidget(self.general_frame, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "JSON editor for diagnosis templates"))
        self.groupBox.setTitle(_translate("MainWindow", "JSON editor"))
        self.treeWidgetDS.headerItem().setText(0, _translate("MainWindow", "Any diagnosis"))
        self.textEditDS.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">  Пункт 1  Пункт 222n,mn,mn,mn,m22</p></body></html>"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionSave.setText(_translate("MainWindow", "Save.."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
