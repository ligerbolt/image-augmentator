# _*_ coding: utf-8 _*_

import sys
import os.path
import cv2
import glob
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mywidgets import (FileListView, ImageView, ConfigButton, CopyConfigDialog,
                        NoiseConfigDialog, FilterConfigDialog, RotateConfigDialog)
from constant import Constant
from image import Image

class AppWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setModeAndParams()

    def initUI(self):
        """レイアウト定義"""
        self.baseLayout = QHBoxLayout()

        """画像表示部定義"""
        self.imgView = ImageView(width=400, height=400)
        self.baseLayout.addWidget(self.imgView)

        """設定部定義"""
        self.sBoxLayout = QGridLayout()
        self.radioGroup = QButtonGroup()
        self.radioBtn1 = QRadioButton("画像コピー")
        self.radioBtn2 = QRadioButton("ノイズ付与")
        self.radioBtn3 = QRadioButton("フィルタリング")
        self.radioBtn4 = QRadioButton("彩度・明度補正")
        self.radioBtn5 = QRadioButton("回転")
        self.radioBtn1.setChecked(True)
        self.confBtn1 = ConfigButton("画像コピー設定", width=150)
        self.confBtn2 = ConfigButton("ノイズ付与設定", width=150)
        self.confBtn3 = ConfigButton("フィルタリング設定", width=150)
        self.confBtn4 = ConfigButton("彩度・明度補正設定", width=150)
        self.confBtn5 = ConfigButton("回転設定", width=150)
        self.confBtn1.clicked.connect(self.__clickedCopyConfButton)
        self.confBtn2.clicked.connect(self.__clickedNoiseConfButton)
        self.confBtn3.clicked.connect(self.__clickedFilterConfButton)
        self.confBtn4.clicked.connect(self.__clickedContrastConfButton)
        self.confBtn5.clicked.connect(self.__clickedRotateConfButton)
        self.radioGroup.addButton(self.radioBtn1)
        self.radioGroup.addButton(self.radioBtn2)
        self.radioGroup.addButton(self.radioBtn3)
        self.radioGroup.addButton(self.radioBtn4)
        self.radioGroup.addButton(self.radioBtn5)
        self.sBoxLayout.addWidget(self.radioBtn1, 0, 0)
        self.sBoxLayout.addWidget(self.radioBtn2, 1, 0)
        self.sBoxLayout.addWidget(self.radioBtn3, 2, 0)
        self.sBoxLayout.addWidget(self.radioBtn4, 3, 0)
        self.sBoxLayout.addWidget(self.radioBtn5, 4, 0)
        self.sBoxLayout.addWidget(self.confBtn1, 0, 1)
        self.sBoxLayout.addWidget(self.confBtn2, 1, 1)
        self.sBoxLayout.addWidget(self.confBtn3, 2, 1)
        self.sBoxLayout.addWidget(self.confBtn4, 3, 1)
        self.sBoxLayout.addWidget(self.confBtn5, 4, 1)

        self.selectGBox = QGroupBox()
        self.selectGBox.setLayout(self.sBoxLayout)

        """リストビュー部定義"""
        self.listView = FileListView()
        self.listView.doubleClicked[QModelIndex].connect(self.__doubleClickedItem)

        """フォルダ選択ボタン定義"""
        secLayout = QVBoxLayout()
        secHLayout = QHBoxLayout()
        secLayout.addWidget(QLabel("画像集合格納ディレクトリ"))
        self.txtLine = QLineEdit()
        self.txtLine.setReadOnly(True)
        self.txtLine.setFixedWidth(300)

        self.secButton = QPushButton('Select')
        self.secButton.setFixedWidth(80)
        self.secButton.clicked.connect(self.__clickedButton)

        secHLayout.addWidget(self.txtLine)
        secHLayout.addWidget(self.secButton)
        secLayout.addLayout(secHLayout)
        secLayout.addWidget(self.selectGBox)
        secLayout.addWidget(self.listView)

        """レイアウトにwidget追加"""
        self.baseLayout.addLayout(secLayout)
        """self.baseLayout.addLayout(self.vlayout)"""
        self.setLayout(self.baseLayout)

        """メインウィンドウ設定・表示"""
        self.setWindowTitle('Image Augmentator')
        self.show()

    def setModeAndParams(self):
        self.copyMode = Constant.LR_REVERSAL_MODE
        self.noiseMode = Constant.SOLT_NOISE_MODE
        self.filterMode = Constant.AVERAGE_FILTER_MODE
        self.noiseParams = {"amount": 0, "alpha": 0}
        self.filterParams = {"ksize": 2, "sigma": 0}
        self.rotateParams = {"angle": 0.0, "scale": 1.0}

    def __clickedButton(self):
        directoryPath = QFileDialog.getExistingDirectory(self,
                '対象画像が入ったフォルダを指定してください', os.path.expanduser('~'))
        self.txtLine.setText(directoryPath)
        self.listView.addFiles(glob.glob(directoryPath + "/*"))
        self.imgView.clear()

    def __doubleClickedItem(self, item):
        if self.radioBtn1.isChecked():
            self.image = Image.reversal(item.data(), self.copyMode)
        elif self.radioBtn2.isChecked():
            self.image = Image.addNoise(item.data(),
                                    self.noiseMode, self.noiseParams)
        elif self.radioBtn3.isChecked():
            self.image = Image.filtering(item.data(),
                                    self.filterMode, self.filterParams)
        elif self.radioBtn5.isChecked():
            self.image = Image.rotate(item.data(), self.rotateParams)
        else:
            pass

        self.imgView.setCvImage(self.image)

    def __clickedCopyConfButton(self):
        confDialog = CopyConfigDialog(mode=self.copyMode)
        if confDialog.exec_() == QDialog.Accepted:
            self.copyMode = confDialog.getSelectedCopyMode()
        else:
            pass

    def __clickedNoiseConfButton(self):
        confDialog = NoiseConfigDialog(mode=self.noiseMode,
                                            params=self.noiseParams)
        if confDialog.exec_() == QDialog.Accepted:
            self.noiseMode, self.noiseParams = confDialog.getSelectedNoiseConfig()
        else:
            pass

    def __clickedFilterConfButton(self):
        confDialog = FilterConfigDialog(mode=self.filterMode,
                                            params=self.filterParams)
        if confDialog.exec_() == QDialog.Accepted:
            self.filterMode, self.filterParams = confDialog.getSelectedFilterConfig()

    def __clickedContrastConfButton(self):
        pass
        """confDialog = ContrastConfigDialog(mode=self.contrastMode,
                                            params=self.contrastParams)"""

    def __clickedRotateConfButton(self):
        confDialog = RotateConfigDialog(params=self.rotateParams)
        if confDialog.exec_() == QDialog.Accepted:
            self.rotateParams = confDialog.getSelectedRotateConfig()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())
