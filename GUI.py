import sys
import cv2
import requests
import json
import base64
import threading
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QGridLayout,
                             QLabel, QPushButton, QComboBox, QMessageBox)
from config import *


# 窗体
class GUI(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

        # data to be post
        self.data = {'access_token': self.token, 'image': '', 'language_type':'CHN_ENG'}

    def initUI(self):
        # 调整窗口大小
        self.resize(400,400)

        # 组件
        self.btupload = QPushButton('upload',self)
        self.btquit   = QPushButton('quit',self)
        self.label    = QLabel()
        self.combo    = QComboBox(self)
        self.combo.addItems(['中英文混合', '英文', '葡萄牙语', '法语', '德语', '意大利语', '西班牙语', '俄语',
                             '日语', '韩语'])

        # 布局
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)
        layout.addWidget(self.btupload, 4, 1, 1, 2)
        layout.addWidget(self.btquit, 4, 3, 1, 2)
        layout.addWidget(self.combo, 5, 1, 1, 2)

        # 设置窗口标题及图标
        self.setWindowTitle('文字识别')
        self.setWindowIcon(QIcon('./icon.jpg'))

        # 设置信号和槽
        self.btquit.clicked.connect(self.close)
        self.btupload.clicked.connect(self.load)
        self.combo.activated[str].connect(self.ChooseLanguage)

        # 尝试获取token
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

        # 判断图片大小是否符合要求
        if 15 <= ImageSize[0] <= 4096 and 15 <= ImageSize[1] <= 4096:
            pass
        else:
            QMessageBox.information(self, 'warining', '图片尺寸过小，无法识别')
            return

        if self.img.size == 1:
            return

        # 显示图片
        self.refresh()
        # 将图片发送到api获得文字信息
        try:
            LoadingBox = QMessageBox()
            LoadingBox.setIcon(QMessageBox.Information)
            LoadingBox.setWindowIcon(QIcon('./icon.jpg'))
            LoadingBox.setWindowTitle('result')
            LoadingBox.setText('识别中')
            LoadingBox.setStandardButtons(QMessageBox.Ok)
            LoadingBox.setDefaultButton(QMessageBox.Ok)
            LoadingBox.exec()
            new_thread = threading.Thread(target=self.GeneralDetect(fileName), name='GetTexts')
            new_thread.start()
            new_thread.join()
        except:
            pass
        # 显示结果
        self.ShowTheResult()

    def refresh(self):
        # 调整图片大小适合窗口尺寸，提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        adjusted_image = cv2.resize(self.img, (400, 300))
        height, width, channel = adjusted_image.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(adjusted_image.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()

        # 将Qimage显示出来
        self.label.setPixmap(QPixmap.fromImage(self.qImg))

    def GetToken(self):
        r = requests.get(token_url)
        #  json解读返回结果
        hjson = json.loads(r.text)
        try:
            self.token = hjson['access_token']
        except KeyError:
            QMessageBox.information(self, hjson['error'], hjson['error_description'])
            raise TimeoutError

    def GeneralDetect(self, filename):
        # 打开文件并进行base64编码
        with open(filename, 'rb') as f:
            base64_data = base64.b64encode(f.read())
        # 判断编码后大小是否符合要求
        if len(base64_data) > 4*1024*1024:
            QMessageBox.information(self, 'warning', '图片过大无法上传')
            raise TimeoutError
        # 将编码后图片存入要发送的数据字典
        self.data['image'] = base64_data
        # 发送请求
        r = requests.post(general_url, headers=header, data=self.data)
        # json解读
        hjson = json.loads(r.text)
        # 将结果放入list
        self.results = []
        for dicts in hjson['words_result']:
            self.results.append(dicts['words'])

    # 选择语种
    def ChooseLanguage(self, text):
        self.data['language_type'] = language_dict[text]

    def ShowTheResult(self):
        # 设置结果提示对话框
        MsBox = QMessageBox()
        MsBox.resize(200, 200)
        MsBox.setIcon(QMessageBox.Information)
        MsBox.setWindowIcon(QIcon('./icon.jpg'))
        MsBox.setWindowTitle('result')
        MsBox.setText('识别结果已放入剪切板')
        MsBox.setInformativeText('如果想看一下结果，也可点击show details')
        # 填充对话框内容
        r_text = ''
        for strings in self.results:
            r_text += strings + '\n'
        MsBox.setDetailedText(r_text)
        MsBox.setStandardButtons(QMessageBox.Ok)
        MsBox.setDefaultButton(QMessageBox.Ok)
        # 将结果放入剪切板
        clip = QApplication.clipboard()
        clip.setText(r_text)

        ret = MsBox.exec()
        if ret == QMessageBox.Ok:
            pass





