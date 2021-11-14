# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ResultImage(object):
    def setupUi(self, ResultImage):
        ResultImage.setObjectName("ResultImage")
        ResultImage.resize(1036, 788)
        self.centralwidget = QtWidgets.QWidget(ResultImage)
        self.centralwidget.setObjectName("centralwidget")
        self.resImage = QtWidgets.QLabel(self.centralwidget)
        self.resImage.setGeometry(QtCore.QRect(38, 34, 961, 701))
        self.resImage.setObjectName("resImage")
        ResultImage.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ResultImage)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1036, 20))
        self.menubar.setObjectName("menubar")
        self.menuSave_Photo = QtWidgets.QMenu(self.menubar)
        self.menuSave_Photo.setObjectName("menuSave_Photo")
        ResultImage.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ResultImage)
        self.statusbar.setObjectName("statusbar")
        ResultImage.setStatusBar(self.statusbar)
        self.actionSave_Photo = QtWidgets.QAction(ResultImage)
        self.actionSave_Photo.setObjectName("actionSave_Photo")
        self.menuSave_Photo.addAction(self.actionSave_Photo)
        self.menubar.addAction(self.menuSave_Photo.menuAction())

        self.retranslateUi(ResultImage)
        QtCore.QMetaObject.connectSlotsByName(ResultImage)

    def retranslateUi(self, ResultImage):
        _translate = QtCore.QCoreApplication.translate
        ResultImage.setWindowTitle(_translate("ResultImage", "Result Image"))
        self.resImage.setText(_translate("ResultImage", "TextLabel"))
        self.menuSave_Photo.setTitle(_translate("ResultImage", "File"))
        self.actionSave_Photo.setText(_translate("ResultImage", "Save Photo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ResultImage = QtWidgets.QMainWindow()
    ui = Ui_ResultImage()
    ui.setupUi(ResultImage)
    ResultImage.show()
    sys.exit(app.exec_())

