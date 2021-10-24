import sys
from os.path import basename
from PyQt5.QtCore import QPoint, Qt, QRect
import webbrowser
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QPushButton, QMenu, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen

import SnippingTool


class Menu(QMainWindow):
    default_title = "Bangla OCR Snipping Tool"

    # numpy_image is the desired image we want to display given as a numpy array.
    def __init__(self, numpy_image=None, snip_number=None, start_position=(1200, 600, 150, 50)):
        super().__init__()

        self.drawing = False
        self.total_snips = 0
        self.title = Menu.default_title

        # New snip
        new_snip_action = QAction('New', self)
        new_snip_action.setShortcut('Ctrl+N')
        new_snip_action.setStatusTip('Snip!')
        new_snip_action.triggered.connect(self.new_snip_window)

        # Exit
        exit_window = QAction('Exit', self)
        exit_window.setShortcut('Ctrl+Q')
        exit_window.setStatusTip('Exit application')
        exit_window.triggered.connect(self.close)

        # About
        about_action = QAction('About', self)
        new_snip_action.setShortcut('Ctrl+N')
        new_snip_action.setStatusTip('About')
        about_action.triggered.connect(lambda: self.about())

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(new_snip_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(about_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(exit_window)

        self.snippingTool = SnippingTool.SnippingWidget()
        self.setGeometry(*start_position)

        if numpy_image is not None and snip_number is not None:
            self.image = self.convert_numpy_img_to_qpixmap(numpy_image)
            self.change_and_set_title("Bangla OCR Snipping Tool")
        else:
            self.image = QPixmap("background.PNG")
            self.change_and_set_title(Menu.default_title)

        self.resize(self.image.width(), self.image.height() + self.toolbar.height())
        self.show()

    
    def new_snip_window(self):
        self.total_snips += 1
        self.snippingTool.start()

    def about(self):
        self.setWindowTitle("Bangla OCR Snipping Tool")
        print("------------------------")
        print("Bangla OCR Snipping Tool")
        print("------------------------")
        print("------Developed By------")
        print("----Jahangir Hossain----")
        print("--------CSE,JnU---------")
        print("---facebook.com/jhm69---")
        webbrowser.open_new("https://facebook.com/jhm69")

    def change_and_set_title(self, new_title):
        self.title = new_title
        self.setWindowTitle(self.title)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = QRect(0, self.toolbar.height(), self.image.width(), self.image.height())
        painter.drawPixmap(rect, self.image)

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def closeEvent(self, event):
        event.accept()

    @staticmethod
    def convert_numpy_img_to_qpixmap(np_img):
        height, width, channel = np_img.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(np_img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())
