import os
import re
import numpy as np

from PyQt5.QtGui import *
from skimage.color.adapt_rgb import adapt_rgb, each_channel
from skimage.color.colorconv import rgb2gray
from skimage.util.dtype import img_as_float, img_as_ubyte
from mainUi import Ui_Image
from resultUi import Ui_ResultImage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PIL import ImageQt, Image

from skimage import io, filters, color, exposure, data

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
    def __init__(self, result):
        super().__init__()
        self.ui = Ui_ResultImage()
        self.result = result
        self.init_ui()
        self.show_result_image(result)

    def init_ui(self):
        self.ui.setupUi(self)
        self.ui.actionSave_Photo.triggered.connect(self.save_result_image)

    def show_result_image(self, result):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.imshow(result)

        toolbar = NavigationToolbar(sc, self)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    # TODO fix save result image
    def save_result_image(self):
        # image = ImageQt.fromqpixmap(self.ui.resImage.pixmap())
        img = self.result.astype(np.uint8)
        image = Image.fromarray(img)
        file_path = QFileDialog.getSaveFileName(self, "Save File", "", "*.jpg")
        image.save(file_path[0])


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Image()
        self.init_ui()

    def init_ui(self):
        self.ui.setupUi(self)

        # connect buttons to functions
        self.ui.actionLoad.triggered.connect(self.load_image)
        self.ui.actionSave.triggered.connect(self.save_image)

        # Filters
        self.ui.actionFarid.triggered.connect(self.farid_image)
        self.ui.actionGabor.triggered.connect(self.gabor_filter)
        self.ui.actionFrangi.triggered.connect(self.frangi_filter)
        self.ui.actionGaussian.triggered.connect(self.gaussian_filter)
        self.ui.actionHessian.triggered.connect(self.hessian_filter)
        self.ui.actionMedian.triggered.connect(self.median_filter)
        self.ui.actionMeijering.triggered.connect(self.meijering_filter)
        self.ui.actionRoberts.triggered.connect(self.roberts_filter)
        self.ui.actionScharr.triggered.connect(self.scharr_filter)
        self.ui.actionSato.triggered.connect(self.sato_filter)
        self.ui.actionShow_Histogram.triggered.connect(self.show_histogram)
        self.ui.actionEqualize_Histogram.triggered.connect(
            self.equalize_histogram)

    def load_image(self):

        print("load image clicked")
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        image_path = file_name[0]
        pixmap = QPixmap(image_path)

        global Image_

        Image_ = io.imread(image_path)

        # self.image = image_path
        self.ui.image.setScaledContents(False)
        self.ui.image.setAlignment(Qt.AlignCenter)

        # Size Problem Fixed
        w = self.ui.image.width()
        h = self.ui.image.height()
        if (pixmap.height() > self.ui.image.height()) or (pixmap.width() > self.ui.image.width()):
            # Tum windowa scale etmek icin
            self.ui.image.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio))
        else:
            self.ui.image.setPixmap(pixmap)

        self.ui.image.installEventFilter(self)

    # fix save image
    def save_image(self):
        imageqt = ImageQt.fromqpixmap(self.ui.image.pixmap())
        file_path = QFileDialog.getSaveFileName(self, "Save File", "", "*.jpg")
        imageqt.save(file_path[0] + file_path[1][1:])

    def open_result_window(self, result):
        self.resWind = ResultWindow(result)
        self.resWind.show()

    # Filters
    def farid_image(self):
        result = filters.farid(rgb2gray(Image_))
        self.open_result_window(result)

    def gabor_filter(self):
        result, real = filters.gabor(rgb2gray(Image_), frequency=0.6)
        self.open_result_window(result)

    def frangi_filter(self):
        result = filters.frangi(rgb2gray(Image_), mode="constant")
        self.open_result_window(result)

    def gaussian_filter(self):
        result = filters.gaussian(rgb2gray(Image_), sigma=3.5)
        self.open_result_window(result)

    def hessian_filter(self):
        result = filters.hessian(rgb2gray(Image_), mode="constant")
        self.open_result_window(result)

    def median_filter(self):
        result = filters.median(rgb2gray(Image_))
        self.open_result_window(result)

    def meijering_filter(self):
        result = filters.meijering(rgb2gray(Image_))
        self.open_result_window(result)

    def roberts_filter(self):
        result = filters.roberts(rgb2gray(Image_))
        self.open_result_window(result)

    def scharr_filter(self):
        result = filters.scharr(rgb2gray(Image_))
        self.open_result_window(result)

    def sato_filter(self):
        result = filters.sato(rgb2gray(Image_), mode="constant")
        self.open_result_window(result)

    # Histograms
    def show_histogram(self):
        # example from -> https://scikit-image.org/docs/stable/auto_examples/applications/plot_rank_filters.html#sphx-glr-auto-examples-applications-plot-rank-filters-py
        # noisy_image = img_as_ubyte(data.camera()) -> works right here
        noisy_image = img_as_ubyte(Image_)
        hist, hist_centers = exposure.histogram(noisy_image)
        plt.figure()
        plt.title("histogram")
        plt.plot(hist_centers, hist, lw=2)
        plt.show()

    def equalize_histogram(self):
        image = img_as_ubyte(Image_)
        image_equalized = exposure.equalize_hist(image) * 255
        hist = np.histogram(image_equalized, bins=np.arange(0, 256))
        a = plt.figure()
        plt.title("histogram")
        plt.plot(hist[1][:-1], hist[0], lw=2)
        # plt.show()
        self.open_result_window(a)


def window():
    import sys
    app = QApplication([])
    win = Window()
    win.show()
    sys.exit(app.exec_())


window()
