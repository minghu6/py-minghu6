# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'os_1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(974, 509)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.outputText = QtGui.QTextBrowser(self.centralwidget)
        self.outputText.setGeometry(QtCore.QRect(50, 20, 511, 261))
        self.outputText.setObjectName(_fromUtf8("outputText"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(580, 50, 160, 211))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.P_Number = QtGui.QLCDNumber(self.verticalLayoutWidget)
        self.P_Number.setObjectName(_fromUtf8("P_Number"))
        self.verticalLayout.addWidget(self.P_Number)
        self.forkButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.forkButton.setObjectName(_fromUtf8("forkButton"))
        self.verticalLayout.addWidget(self.forkButton)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(40, 340, 691, 101))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(740, 332, 141, 112))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.SocketSendButton = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.SocketSendButton.setObjectName(_fromUtf8("SocketSendButton"))
        self.verticalLayout_2.addWidget(self.SocketSendButton)
        self.FIFOPipeSendButton = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.FIFOPipeSendButton.setObjectName(_fromUtf8("FIFOPipeSendButton"))
        self.verticalLayout_2.addWidget(self.FIFOPipeSendButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 974, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menuInfo = QtGui.QMenu(self.menubar)
        self.menuInfo.setObjectName(_fromUtf8("menuInfo"))
        self.menuAuthor = QtGui.QMenu(self.menuInfo)
        self.menuAuthor.setObjectName(_fromUtf8("menuAuthor"))
        MainWindow.setMenuBar(self.menubar)
        self.actionUnImplemented = QtGui.QAction(MainWindow)
        self.actionUnImplemented.setObjectName(_fromUtf8("actionUnImplemented"))
        self.actionZhuangyuan = QtGui.QAction(MainWindow)
        self.actionZhuangyuan.setObjectName(_fromUtf8("actionZhuangyuan"))
        self.menu.addAction(self.actionUnImplemented)
        self.menu.addSeparator()
        self.menuAuthor.addAction(self.actionZhuangyuan)
        self.menuInfo.addSeparator()
        self.menuInfo.addAction(self.menuAuthor.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.forkButton.setText(_translate("MainWindow", "Fork", None))
        self.SocketSendButton.setText(_translate("MainWindow", "SocketSend", None))
        self.FIFOPipeSendButton.setText(_translate("MainWindow", "FIFOPipeSend", None))
        self.menu.setTitle(_translate("MainWindow", "Menu", None))
        self.menuInfo.setTitle(_translate("MainWindow", "Info", None))
        self.menuAuthor.setTitle(_translate("MainWindow", "Author", None))
        self.actionUnImplemented.setText(_translate("MainWindow", "UnImplemented", None))
        self.actionZhuangyuan.setText(_translate("MainWindow", "Zhuangyuan", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

