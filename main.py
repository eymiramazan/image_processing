import os
from pathlib import PosixPath
import time
import re
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_qt5 import FigureCanvasQT
import numpy as np
import warnings
from PyQt5.QtGui import *
from skimage.color.adapt_rgb import adapt_rgb, each_channel
from skimage.color.colorconv import rgb2gray
from skimage.util.dtype import img_as_float, img_as_ubyte
from mainUi import Ui_Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PIL import ImageQt, Image

from skimage import io, filters, color, exposure, data, transform

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure, SubplotParams


# For matplotlib into result window
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_axis_off()
        super(MplCanvas, self).__init__(fig)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        warnings.filterwarnings("ignore")
        self.Processed_ = None
        self.Image_ = None
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
        self.ui.actionResizing.triggered.connect(self.resize_image)
        self.ui.actionRotation.triggered.connect(self.rotate)
        self.ui.actionCropping.triggered.connect(self.crop)
        self.ui.actionSwirl.triggered.connect(self.swirl_image)
        # self.ui.actionPyramid_Reduce.triggered.connnect(self.pyramid_reduce)

    def load_image(self):

        print("load image clicked")
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        self.Image_path = file_name[0]
        pixmap = QPixmap(self.Image_path)

        self.Image_ = io.imread(self.Image_path)
        self.Processed_ = self.Image_

        # self.image = self.Image_path
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

    def show_image(self, result):
        self.ui.image.setScaledContents(False)
        self.ui.image.setAlignment(Qt.AlignCenter)

        im = Image.fromarray(result)
        data = im.tostring('raw', 'RGBA')
        image = QImage(data, im.size[0], im.size[1], QImage.Format_ARGB32)
        pix = QPixmap.fromImage(image)
        self.ui.image.setPixmap(pix)
        self.ui.image.installEventFilter(self)

        # canvas = MplCanvas(self, width=8, height=6, dpi=100)
        # canvas.axes.imshow(result)
        # canvas.draw()
        # size = canvas.size()
        # width, height = size.width(), size.height()
        # img = QImage(canvas.buffer_rgba(), width, height, QImage.Format_RGB32)
        # pixmap = QPixmap(img)
        # w = self.ui.image.width()
        # h = self.ui.image.height()
        # if (pixmap.height() > self.ui.image.height()) or (pixmap.width() > self.ui.image.width()):
        #     # Tum windowa scale etmek icin
        #     self.ui.image.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio))
        # else:
        #     self.ui.image.setPixmap(pixmap)

        # self.ui.image.installEventFilter(self)

    # Filters
    def farid_image(self):
        result = filters.farid(rgb2gray(self.Processed_))
        self.Processed_ = result
        self.show_image(self.Processed_)

    def gabor_filter(self):
        result, real = filters.gabor(rgb2gray(self.Processed_), frequency=0.6)
        self.Processed_ = result
        self.show_image(self.Processed_)

    def frangi_filter(self):
        result = filters.frangi(rgb2gray(self.Processed_), mode="constant")
        self.Processed_ = result
        self.show_image(self.Processed_)

    def gaussian_filter(self):
        result = filters.gaussian(rgb2gray(self.Processed_), sigma=3.5)
        self.Processed_ = result
        self.show_image(self.Processed_)

    def hessian_filter(self):
        result = filters.hessian(rgb2gray(self.Processed_), mode="constant")
        self.Processed_ = result
        self.show_image(self.Processed_)

    def median_filter(self):
        result = filters.median(rgb2gray(self.Processed_))
        self.Processed_ = result
        self.show_image(self.Processed_)

    def meijering_filter(self):
        result = filters.meijering(rgb2gray(self.Processed_))
        self.Processed_ = result
        self.show_image(self.Processed_)

    def roberts_filter(self):
        result = filters.roberts(rgb2gray(self.Processed_))
        self.Processed_ = result
        self.show_image(self.Processed_)

    def scharr_filter(self):
        result = filters.scharr(rgb2gray(self.Processed_))
        self.Processed_ = result
        self.show_image(self.Processed_)

    def sato_filter(self):
        result = filters.sato(rgb2gray(self.Processed_), mode="constant")
        self.Processed_ = result
        self.show_image(self.Processed_)

    # Histograms
    def show_histogram(self):
        # example from -> https://scikit-image.org/docs/stable/auto_examples/applications/plot_rank_filters.html#sphx-glr-auto-examples-applications-plot-rank-filters-py
        # noisy_image = img_as_ubyte(data.camera()) -> works right here
        noisy_image = img_as_ubyte(self.Image_)
        hist, hist_centers = exposure.histogram(noisy_image)
        plt.figure()
        plt.title("histogram")
        plt.plot(hist_centers, hist, lw=2)
        plt.show()

    def equalize_histogram(self):
        image = img_as_ubyte(self.Image_)
        self.Image_equalized = exposure.equalize_hist(image) * 255
        hist = np.histogram(self.Image_equalized, bins=np.arange(0, 256))
        a = plt.figure()
        plt.title("histogram")
        plt.plot(hist[1][:-1], hist[0], lw=2)
        plt.show()

    # Transforms
    def resize_image(self):
        result = transform.resize(self.Processed_, (100, 100))
        self.Processed_ = result
        self.show_image(result)

    def rotate(self):
        result = transform.rotate(self.Processed_, 2)
        self.Processed_ = result
        self.show_image(self.Processed_)

    def crop(self):
        self.Processed_ = self.Processed_[144:358, 620:801]
        self.show_image(self.Processed_)

    def swirl_image(self):
        # result = transform.swirl(self.Processed_)
        # self.Processed_ = result
        self.show_image(self.Processed_)


def window():
    import sys
    app = QApplication([])
    win = Window()
    win.show()
    sys.exit(app.exec_())


window()
