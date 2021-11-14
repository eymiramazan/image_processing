# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Image(object):
    def setupUi(self, Image):
        Image.setObjectName("Image")
        Image.resize(1128, 888)
        self.centralwidget = QtWidgets.QWidget(Image)
        self.centralwidget.setObjectName("centralwidget")
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(40, 70, 1024, 720))
        self.image.setMaximumSize(QtCore.QSize(1920, 1080))
        self.image.setTextFormat(QtCore.Qt.PlainText)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setWordWrap(True)
        self.image.setObjectName("image")
        Image.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Image)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFilters = QtWidgets.QMenu(self.menubar)
        self.menuFilters.setObjectName("menuFilters")
        self.menuHistogram = QtWidgets.QMenu(self.menubar)
        self.menuHistogram.setObjectName("menuHistogram")
        self.menuTransforms = QtWidgets.QMenu(self.menubar)
        self.menuTransforms.setObjectName("menuTransforms")
        self.menuIntensity = QtWidgets.QMenu(self.menubar)
        self.menuIntensity.setObjectName("menuIntensity")
        self.menuMorphology = QtWidgets.QMenu(self.menubar)
        self.menuMorphology.setObjectName("menuMorphology")
        Image.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Image)
        self.statusbar.setObjectName("statusbar")
        Image.setStatusBar(self.statusbar)
        self.actionLoad = QtWidgets.QAction(Image)
        self.actionLoad.setObjectName("actionLoad")
        self.actionSave = QtWidgets.QAction(Image)
        self.actionSave.setObjectName("actionSave")
        self.actionFarid = QtWidgets.QAction(Image)
        self.actionFarid.setObjectName("actionFarid")
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFilters.addAction(self.actionFarid)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFilters.menuAction())
        self.menubar.addAction(self.menuHistogram.menuAction())
        self.menubar.addAction(self.menuTransforms.menuAction())
        self.menubar.addAction(self.menuIntensity.menuAction())
        self.menubar.addAction(self.menuMorphology.menuAction())

        self.retranslateUi(Image)
        QtCore.QMetaObject.connectSlotsByName(Image)

    def retranslateUi(self, Image):
        _translate = QtCore.QCoreApplication.translate
        Image.setWindowTitle(_translate("Image", "MainWindow"))
        self.image.setText(_translate("Image", "To Upload Image File -> Load"))
        self.menuFile.setTitle(_translate("Image", "File"))
        self.menuFilters.setTitle(_translate("Image", "Filters"))
        self.menuHistogram.setTitle(_translate("Image", "Histogram"))
        self.menuTransforms.setTitle(_translate("Image", "Transforms"))
        self.menuIntensity.setTitle(_translate("Image", "Intensity"))
        self.menuMorphology.setTitle(_translate("Image", "Morphology"))
        self.actionLoad.setText(_translate("Image", "Load"))
        self.actionSave.setText(_translate("Image", "Save As"))
        self.actionFarid.setText(_translate("Image", "Farid"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Image = QtWidgets.QMainWindow()
    ui = Ui_Image()
    ui.setupUi(Image)
    Image.show()
    sys.exit(app.exec_())

