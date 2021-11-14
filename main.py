import os
import re
import numpy as np

from PyQt5.QtGui import *
from skimage.color.colorconv import rgb2gray
from mainUi import Ui_Image
from resultUi import Ui_ResultImage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PIL import ImageQt,Image

from skimage import io,filters,color

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# For matplotlib into result window
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)



class ResultWindow(QMainWindow):
    def __init__(self,result):
        super().__init__()
        self.ui = Ui_ResultImage()
        self.init_ui()
        self.show_result_image(result)
    
    def init_ui(self):
        self.ui.setupUi(self)
        self.ui.actionSave_Photo.triggered.connect(self.save_result_image)
    
    def show_result_image(self,result):
        sc = MplCanvas(self,width=5, height=4,dpi=100)
        sc.axes.imshow(result)

        toolbar = NavigationToolbar(sc,self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def save_result_image(self):
        image = ImageQt.fromqpixmap(self.ui.resImage.pixmap())
        file_path = QFileDialog.getSaveFileName(self, "Save File", "", "*.jpg")
        image.save(file_path[0] + file_path[1][1:])


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Image()
        self.init_ui()

    def init_ui(self):
        self.ui.setupUi(self)
        self.ui.actionLoad.triggered.connect(self.load_image)
        self.ui.actionSave.triggered.connect(self.save_image)

        # Filters
        self.ui.actionFarid.triggered.connect(self.farid_image)

    def button_clicked(self):
        print("clicked!")
        self.ui.label.setText("deneme")
        self.update()

    def load_image(self):

        print("load image clicked")
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        image_path = file_name[0]
        pixmap = QPixmap(image_path)

        global Image_ 

        Image_ = io.imread(image_path)

        self.image = image_path
        self.ui.image.setScaledContents(False)
        self.ui.image.setAlignment(Qt.AlignCenter)

        # Size Problem Fixed
        w = self.ui.image.width()
        h = self.ui.image.height()
        if (pixmap.height() > self.ui.image.height()) or (pixmap.width() > self.ui.image.width()) :
            # Tum windowa scale etmek icin
            self.ui.image.setPixmap(pixmap.scaled(w,h,Qt.KeepAspectRatio))
        else:
            self.ui.image.setPixmap(pixmap)
            
        self.ui.image.installEventFilter(self)

    # fix save image
    def save_image(self):
        imageqt = ImageQt.fromqpixmap(self.ui.image.pixmap())
        file_path = QFileDialog.getSaveFileName(self, "Save File", "", "*.jpg")
        imageqt.save(file_path[0] + file_path[1][1:])

    
    def open_result_window(self,result):
        self.resWind = ResultWindow(result)
        self.resWind.show()

    # Filters
    def farid_image(self):
        result = filters.farid(rgb2gray(Image_))
        self.open_result_window(result)
        



def window():
    import sys
    app = QApplication([])
    win = Window()
    win.show()
    sys.exit(app.exec_())


window()