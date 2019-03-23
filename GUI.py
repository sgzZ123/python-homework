import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton)


class GUI(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400,400)

        self.btupload = QPushButton('upload',self)
        self.btquit   = QPushButton('quit',self)
        self.label    = QLabel()

        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)
        layout.addWidget(self.btupload, 4, 1, 1, 2)
        layout.addWidget(self.btquit, 4, 3, 1, 2)

        self.btquit.clicked.connect(self.close)
        self.btupload.clicked.connect(self.load)

    def load(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        # 采用opencv函数读取数据
        self.img = cv2.imread(fileName, -1)

        if self.img.size == 1:
            return

        self.refresh()

    def refresh(self):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 将Qimage显示出来
        self.label.setPixmap(QPixmap.fromImage(self.qImg))


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(a.exec_())


