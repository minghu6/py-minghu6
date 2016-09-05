# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'os_2.ui'
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
        MainWindow.resize(668, 573)
        MainWindow.setDocumentMode(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 291, 471))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.busTextBrowser = QtGui.QTextBrowser(self.verticalLayoutWidget)
        self.busTextBrowser.setObjectName(_fromUtf8("busTextBrowser"))
        self.verticalLayout.addWidget(self.busTextBrowser)
        self.go_busButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.go_busButton.setObjectName(_fromUtf8("go_busButton"))
        self.verticalLayout.addWidget(self.go_busButton)
        self.end_busButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.end_busButton.setObjectName(_fromUtf8("end_busButton"))
        self.verticalLayout.addWidget(self.end_busButton)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(350, 30, 281, 411))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.sell_ticketTextBrowser = QtGui.QTextBrowser(self.verticalLayoutWidget_2)
        self.sell_ticketTextBrowser.setObjectName(_fromUtf8("sell_ticketTextBrowser"))
        self.verticalLayout_2.addWidget(self.sell_ticketTextBrowser)
        self.formLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(350, 440, 141, 81))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.formLayoutWidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.sell_ticket_casualButton = QtGui.QPushButton(self.formLayoutWidget)
        self.sell_ticket_casualButton.setObjectName(_fromUtf8("sell_ticket_casualButton"))
        self.verticalLayout_3.addWidget(self.sell_ticket_casualButton)
        self.sell_ticket_restrictButton = QtGui.QPushButton(self.formLayoutWidget)
        self.sell_ticket_restrictButton.setObjectName(_fromUtf8("sell_ticket_restrictButton"))
        self.verticalLayout_3.addWidget(self.sell_ticket_restrictButton)
        self.end_sell_ticketButton = QtGui.QPushButton(self.centralwidget)
        self.end_sell_ticketButton.setGeometry(QtCore.QRect(500, 460, 75, 31))
        self.end_sell_ticketButton.setObjectName(_fromUtf8("end_sell_ticketButton"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 231, 20))
        self.label.setStyleSheet(_fromUtf8("font: 75 italic 9pt \"Arial\";"))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 10, 61, 16))
        self.label_2.setStyleSheet(_fromUtf8("font: 9pt \"Fixedsys\";\n"
"font: 10pt \"Arial\";\n"
"font: 75 italic 9pt \"Arial\";"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.spinBox = QtGui.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(560, 0, 71, 22))
        self.spinBox.setMaximum(1000)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(440, 0, 91, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 668, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuInformation = QtGui.QMenu(self.menubar)
        self.menuInformation.setObjectName(_fromUtf8("menuInformation"))
        self.menuAuthor = QtGui.QMenu(self.menuInformation)
        self.menuAuthor.setObjectName(_fromUtf8("menuAuthor"))
        MainWindow.setMenuBar(self.menubar)
        self.actionZhuangyuan = QtGui.QAction(MainWindow)
        self.actionZhuangyuan.setObjectName(_fromUtf8("actionZhuangyuan"))
        self.menuAuthor.addAction(self.actionZhuangyuan)
        self.menuInformation.addAction(self.menuAuthor.menuAction())
        self.menubar.addAction(self.menuInformation.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.go_busButton.setText(_translate("MainWindow", "Go", None))
        self.end_busButton.setText(_translate("MainWindow", "End", None))
        self.sell_ticket_casualButton.setText(_translate("MainWindow", "Casual-selling", None))
        self.sell_ticket_restrictButton.setText(_translate("MainWindow", "In-Order-selling", None))
        self.end_sell_ticketButton.setText(_translate("MainWindow", "End", None))
        self.label.setText(_translate("MainWindow", "Driver-Conductor", None))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">sell ticket </span></p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-style:italic; color:#0000ff;\">Processnumber</span></p></body></html>", None))
        self.menuInformation.setTitle(_translate("MainWindow", "Information", None))
        self.menuAuthor.setTitle(_translate("MainWindow", "Author", None))
        self.actionZhuangyuan.setText(_translate("MainWindow", "Zhuangyuan", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

