import os
from pathlib import PosixPath
import time
import re
import numpy as np
import warnings
import cv2
from PyQt5.QtGui import *
from numpy.lib import interp
from scipy.ndimage import interpolation
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
        self.image = None
        self.processed = None
        self.image_path = None
        self.ui = Ui_Image()
        self.init_ui()

    def init_ui(self):
        self.ui.setupUi(self)

        # connect buttons to functions
        self.ui.actionLoad.triggered.connect(self.load_image)
        self.ui.actionSave.triggered.connect(self.save_image)
        self.ui.resetImage.clicked.connect(self.reset_image)

        # Filters
        self.ui.actionFarid.triggered.connect(self.laplacian_filter)
        self.ui.actionGabor.triggered.connect(self.blur_filter)
        self.ui.actionFrangi.triggered.connect(self.bilateral_filter)
        self.ui.actionGaussian.triggered.connect(self.gaussian_filter)
        self.ui.actionHessian.triggered.connect(self.threshold)
        self.ui.actionMedian.triggered.connect(self.median_filter)
        self.ui.actionMeijering.triggered.connect(self.box_filter)
        self.ui.actionRoberts.triggered.connect(self.sobel_filter)
        self.ui.actionScharr.triggered.connect(self.scharr_filter)
        self.ui.actionSato.triggered.connect(self.dilate_filter)
        # histograms
        self.ui.actionShow_Histogram.triggered.connect(self.show_histogram)
        self.ui.actionEqualize_Histogram.triggered.connect(
            self.equalize_histogram)
        # transforms
        self.ui.actionResizing.triggered.connect(self.resize_image)
        self.ui.actionRotation.triggered.connect(self.rotate)
        self.ui.actionCropping.triggered.connect(self.crop)
        self.ui.actionSwirl.triggered.connect(self.warp_image)
        self.ui.actionPyramid_Reduce.triggered.connect(self.warp_perspective)
        # intensity
        self.ui.actionNegative.triggered.connect(self.negative)
        self.ui.actionLogarithmic.triggered.connect(self.logarithmic)
        self.ui.actionPower_Law.triggered.connect(self.powerlaw)
        # morfolojik
        self.ui.actionErosion.triggered.connect(self.erosion)
        self.ui.actionDilation.triggered.connect(self.dilation)
        self.ui.actionOpening.triggered.connect(self.opening)
        self.ui.actionClosing.triggered.connect(self.closing)
        self.ui.actionMorphological_Gradient.triggered.connect(
            self.morf_gradient)
        self.ui.actionTop_Hat.triggered.connect(self.top_hat)
        self.ui.actionBlack_Hat.triggered.connect(self.black_hat)
        self.ui.actionSquare.triggered.connect(self.square)
        self.ui.actionSkeletonize.triggered.connect(self.skeletonize)
        self.ui.actionFloodFill.triggered.connect(self.flood_fill)
        #video
        self.ui.actionWebCam.triggered.connect(self.canny_edge_webcam)
        self.ui.actionVideo.triggered.connect(self.canny_edge_video)
        
    
    # Load Image
    def load_image(self):
        print("load image clicked")
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        self.image = cv2.imread(file_name[0])
        self.image_path = file_name[0]
        self.set_photo(self.image)
        
    # Save image
    def save_image(self):
        file_path = QFileDialog.getSaveFileName(self, "Save File", "", "*.jpg")
        cv2.imwrite(file_path[0], self.processed)
        print("saved")

    def reset_image(self):
        self.processed = self.image
        self.set_photo(self.processed)
        
    def get_user_input(self, input_type):
        dialog = QInputDialog.getInt(
            self, "User Input", input_type, 0, 0, 1024, 1)
        return dialog

    def set_photo(self, image):
        self.processed = image
        cv2_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2_image = QImage(
            cv2_image, cv2_image.shape[1], cv2_image.shape[0], cv2_image.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(cv2_image)
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


    # Filters
    def laplacian_filter(self):
        result = cv2.Laplacian(self.processed, cv2.CV_16S, ksize=3)
        result = cv2.convertScaleAbs(result)
        self.set_photo(result)

    def blur_filter(self):
        result = cv2.blur(self.processed, (5, 5))
        self.set_photo(result)

    def bilateral_filter(self):
        result = cv2.bilateralFilter(self.processed, 9, 75, 75)
        self.set_photo(result)

    def gaussian_filter(self):
        result = cv2.GaussianBlur(
            self.processed, (5, 5), cv2.BORDER_DEFAULT)
        self.set_photo(result)

    def threshold(self):
        ret, result = cv2.threshold(
            self.processed, 127, 255, cv2.THRESH_BINARY)
        self.set_photo(result)

    def median_filter(self):
        result = cv2.medianBlur(self.processed, 5)
        self.set_photo(result)

    def box_filter(self):
        result = cv2.boxFilter(self.processed, -1, (31, 31))
        self.set_photo(result)

    def sobel_filter(self):
        gray = cv2.cvtColor(self.processed, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3,
                           scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3,
                           scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        self.set_photo(grad)

    def scharr_filter(self):
        scharrx_filter = cv2.Scharr(
            self.processed, ddepth=-1, dx=1, dy=0, scale=1, borderType=cv2.BORDER_DEFAULT)
        scharry_filter = cv2.Scharr(
            self.processed, ddepth=-1, dx=0, dy=1, scale=1, borderType=cv2.BORDER_DEFAULT)

        scharr_filter = scharrx_filter + scharry_filter
        self.set_photo(scharr_filter)

    def dilate_filter(self):
        kernel = np.ones((5, 5), 'uint8')
        result = cv2.dilate(self.processed, kernel, iterations=1)
        self.set_photo(result)
    
    
    
    # Histograms
    def show_histogram(self):
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([self.processed], [i], None, [256], [0, 256])
            plt.plot(histr, color=col)
            plt.xlim([0, 256])
        plt.show()

    def equalize_histogram(self):
        image = cv2.imread(self.image_path, 0)
        equalized = cv2.equalizeHist(image)
        res = np.hstack((image, equalized))  # stacking images side-by-side
        self.set_photo(res)
    
    
    
    # Transforms
    def resize_image(self):
        width = int(self.get_user_input("width")[0])
        height = int(self.get_user_input("height")[0])
        dim = (width, height)
        result = cv2.resize(self.processed, dim, interpolation=cv2.INTER_AREA)
        self.set_photo(result)

    def rotate(self):
        result = cv2.rotate(self.processed, cv2.ROTATE_90_CLOCKWISE)
        self.set_photo(result)

    def crop(self):
        upper_left = int(self.processed.shape[0] * 0.05)
        lower_left = int(self.processed.shape[0] * 0.8)
        upper_right = int(self.processed.shape[1] * 0.05)
        lower_right = int(self.processed.shape[1] * 0.8)
        result = self.processed[upper_left:lower_left, upper_right:lower_right]
        self.set_photo(result)

    def warp_image(self):
        rows, cols, ch = self.processed.shape
        M = np.float32([[1, 0, 100], [0, 1, 50]])
        result = cv2.warpAffine(self.processed, M, (cols, rows))
        self.set_photo(result)

    def warp_perspective(self):
        num_rows, num_cols = self.processed.shape[:2]
        src_points = np.float32(
            [[0, 0], [num_cols-1, 0], [0, num_rows-1], [num_cols-1, num_rows-1]])
        dst_points = np.float32(
            [[0, 0], [num_cols-1, 0], [int(0.33*num_cols), num_rows-1], [int(0.66*num_cols), num_rows-1]])
        projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        result = cv2.warpPerspective(
            self.processed, projective_matrix, (num_cols, num_rows))
        self.set_photo(result)
    
    # Yogunluk Donusumu
    
    def negative(self):
        negative = cv2.bitwise_not(self.processed)
        self.set_photo(negative)
    
    def logarithmic(self):
        logarithmic = (np.log(self.processed+1)/(np.log(1+np.max(self.processed))))*255
        logarithmic = np.array(logarithmic,dtype=np.uint8)
        self.set_photo(logarithmic)
        
    def powerlaw(self):
        gamma = int(self.get_user_input("gamma")[0])
        powerlaw = np.array(255*(self.processed / 255) ** gamma, dtype = 'uint8')
        self.set_photo(powerlaw)
    
    
    # Morfolojik
    def erosion(self):
        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(self.processed, kernel, iterations=1)
        self.set_photo(erosion)

    def dilation(self):
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(self.processed, kernel, iterations=1)
        self.set_photo(dilation)

    def opening(self):
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(self.processed, cv2.MORPH_OPEN, kernel)
        self.set_photo(opening)

    def closing(self):
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(self.processed, cv2.MORPH_CLOSE, kernel)
        self.set_photo(closing)

    def morf_gradient(self):
        kernel = np.ones((5, 5), np.uint8)
        gradient = cv2.morphologyEx(self.processed, cv2.MORPH_GRADIENT, kernel)
        self.set_photo(gradient)

    def top_hat(self):
        kernel = np.ones((5, 5), np.uint8)
        tophat = cv2.morphologyEx(self.processed, cv2.MORPH_TOPHAT, kernel)
        self.set_photo(tophat)

    def black_hat(self):
        kernel = np.ones((5, 5), np.uint8)
        blackhat = cv2.morphologyEx(self.processed, cv2.MORPH_BLACKHAT, kernel)
        self.set_photo(blackhat)

    def square(self):
        start_point = (5, 5)
        end_point = (220, 220)
        color = (255, 220, 20)
        thickness = 3
        result = cv2.rectangle(self.processed, start_point,
                               end_point, color, thickness)
        self.set_photo(result)

    def skeletonize(self):
        img = cv2.imread(self.image_path, 0)
        size = np.size(img)
        skel = np.zeros(img.shape, np.uint8)

        ret, img = cv2.threshold(img, 127, 255, 0)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        done = False

        while(not done):
            eroded = cv2.erode(img, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(img, temp)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded.copy()

            zeros = size - cv2.countNonZero(img)
            if zeros == size:
                done = True

        self.set_photo(skel)

    def flood_fill(self):
        image = cv2.imread(self.image_path, 0)
        height, width = image.shape
        nelem = 0
        for x in range(height):
            for y in range(width):
                if image[x, y] == 255:
                    nelem += 1
                    cv2.floodFill(image, None, (y, x), nelem)

        print("Number of elements: ", nelem)

        self.set_photo(image)
        
    
    def canny_edge_webcam(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            canny = cv2.Canny(blur, 10, 70)
            ret, mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
            cv2.imshow('Webcam Canny Edge', mask)
            
            # Exit with Enter Button
            if cv2.waitKey(1) == 13:
                break
        cap.release()
        cv2.destroyAllWindows()
        
    def canny_edge_video(self):
        cap = cv2.VideoCapture(QFileDialog.getOpenFileName(filter="Image (*.*)")[0])
        frame_counter = 0
        while True:
            ret, img = cap.read()
            frame_counter += 1
            if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                frame_counter = 0 
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            if (len(img.shape) == 3):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            canny = cv2.Canny(blur, 10, 70)
            ret, mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
            cv2.imshow('Video Canny Edge', mask)
            
            # Exit with Enter Button
            if cv2.waitKey(1) == 13:
                break
        cap.release()
        cv2.destroyAllWindows()
            


def window():
    import sys
    app = QApplication([])
    win = Window()
    win.show()
    sys.exit(app.exec_())


window()
