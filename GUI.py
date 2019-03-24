import sys
import cv2
import requests
import json
import base64
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QComboBox, QMessageBox)
from config import *


class GUI(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_handwriting = False
        self.data = {'access_token': self.token, 'image': '', 'language_type':'CHN_ENG'}

    def initUI(self):
        self.resize(400,400)

        self.btupload = QPushButton('upload',self)
        self.btquit   = QPushButton('quit',self)
        self.label    = QLabel()
        self.combo    = QComboBox(self)
        self.combo.addItems(['中英文混合', '英文', '葡萄牙语', '法语', '德语', '意大利语', '西班牙语', '俄语',
                             '日语', '韩语'])

        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)
        layout.addWidget(self.btupload, 4, 1, 1, 2)
        layout.addWidget(self.btquit, 4, 3, 1, 2)
        layout.addWidget(self.combo, 5, 1, 1, 2)

        self.setWindowTitle('文字识别')
        self.setWindowIcon(QIcon('./icon.jpg'))

        self.btquit.clicked.connect(self.close)
        self.btupload.clicked.connect(self.load)
        self.combo.activated[str].connect(self.ChooseLanguage)

        try:
            self.GetToken()
        except:
            self.close()

    def load(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './', '*.png *.jpg *.bmp')

        if fileName is '':
            return

        # 采用opencv函数读取数据
        self.img = cv2.imread(fileName, -1)
        ImageSize = self.img.shape
        if 15 <= ImageSize[0] <= 4096 and 15 <= ImageSize[1] <= 4096:
            pass
        else:
            QMessageBox.information(self, 'warining', '图片尺寸过小，无法识别')
            return

        if self.img.size == 1:
            return
        self.refresh()
        try:
            self.GeneralDeteect(fileName)
        except:
            pass

        self.ShowTheResult()

    def refresh(self):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        adjusted_image = cv2.resize(self.img, (400, 300))
        height, width, channel = adjusted_image.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(adjusted_image.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 将Qimage显示出来
        self.label.setPixmap(QPixmap.fromImage(self.qImg))

    def GetToken(self):
        r = requests.get(token_url)
        hjson = json.loads(r.text)
        try:
            self.token = hjson['access_token']
        except KeyError:
            QMessageBox.information(self, hjson['error'], hjson['error_description'])
            raise TimeoutError

    def GeneralDeteect(self, filename):
        with open(filename, 'rb') as f:
            base64_data = base64.b64encode(f.read())

        if len(base64_data) > 4*1024*1024:
            QMessageBox.information(self, 'warning', '图片过大无法上传')
            raise TimeoutError

        self.data['image'] = base64_data

        r = requests.post(general_url, headers=header, data=self.data)

        hjson = json.loads(r.text)

        self.results = []

        for dicts in hjson['words_result']:
            self.results.append(dicts['words'])

    def ChooseLanguage(self, text):
        self.data['language_type'] = language_dict[text]

    def ShowTheResult(self):
        MsBox = QMessageBox()
        MsBox.resize(200, 200)
        MsBox.setIcon(QMessageBox.Information)
        MsBox.setWindowIcon(QIcon('./icon.jpg'))
        MsBox.setWindowTitle('result')
        MsBox.setText('识别结果已放入剪切板')
        MsBox.setInformativeText('如果想看一下结果，也可点击show details')

        r_text = ''
        for strings in self.results:
            r_text += strings + '\n'
        MsBox.setDetailedText(r_text)
        MsBox.setStandardButtons(QMessageBox.Ok)
        MsBox.setDefaultButton(QMessageBox.Ok)

        clip = QApplication.clipboard()
        clip.setText(r_text)

        ret = MsBox.exec()
        if ret == QMessageBox.Ok:
            pass





