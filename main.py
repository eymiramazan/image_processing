from PyQt5.QtGui import *
from mainUi import Ui_Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Image()
        self.init_ui()

    def init_ui(self):
        self.ui.setupUi(self)
        self.ui.actionLoad.triggered.connect(self.load_image)
        self.ui.actionSave.triggered.connect(self.save_image)

    def button_clicked(self):
        print("clicked!")
        self.ui.label.setText("deneme")
        self.update()

    def load_image(self):
        # TODO foto fix size olarak yukleniyor onu ayarlamak lazım
        print("load image clicked")
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        image_path = file_name[0]
        pixmap = QPixmap(image_path)
        self.image = image_path
        self.ui.image.setScaledContents(True)
        self.ui.image.setAlignment(Qt.AlignCenter)
        self.ui.image.setPixmap(pixmap)
        self.ui.image.installEventFilter(self)

    def save_image(self):
        print("save image")
        p = self.ui.image.pixmap()
        file_path = QFileDialog.getSaveFileName(self, "Save File", "", "*.jpg")
        print("aaaaaaaaaaaaa")
        print(file_path[0])
        p.save(file_path[0])


def window():
    import sys
    app = QApplication([])
    win = Window()
    win.show()
    sys.exit(app.exec_())


window()
