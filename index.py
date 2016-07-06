# _*_ coding: utf-8 _*_

import sys
import os.path
import cv2
import glob
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mywidgets import FileListView, ImageView, ConfigButton, CopyConfigDialog, NoiseConfigDialog

class AppWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setRunningMode()

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
        self.confBtn1 = ConfigButton("画像コピー設定", width=150)
        self.confBtn2 = ConfigButton("ノイズ付与設定", width=150)
        self.confBtn3 = ConfigButton("フィルタリング設定", width=150)
        self.confBtn1.clicked.connect(self.__clickedCopyConfButton)
        self.confBtn2.clicked.connect(self.__clickedNoiseConfButton)
        self.confBtn3.clicked.connect(self.__clickedCopyConfButton)
        self.radioGroup.addButton(self.radioBtn1)
        self.radioGroup.addButton(self.radioBtn2)
        self.radioGroup.addButton(self.radioBtn3)
        self.sBoxLayout.addWidget(self.radioBtn1, 0, 0)
        self.sBoxLayout.addWidget(self.radioBtn2, 1, 0)
        self.sBoxLayout.addWidget(self.radioBtn3, 2, 0)
        self.sBoxLayout.addWidget(self.confBtn1, 0, 1)
        self.sBoxLayout.addWidget(self.confBtn2, 1, 1)
        self.sBoxLayout.addWidget(self.confBtn3, 2, 1)

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
        self.setWindowTitle('Image Copy')
        self.show()

    def setRunningMode(self):
        self.copyMode = None
        self.noiseMode = None
        self.noiseParams = 0

    def __clickedButton(self):
        directoryPath = QFileDialog.getExistingDirectory(self,
                '対象画像が入ったフォルダを指定してください', os.path.expanduser('~'))
        self.txtLine.setText(directoryPath)
        self.listView.addFiles(glob.glob(directoryPath + "/*"))
        self.imgView.clear()

    def __doubleClickedItem(self, item):
        self.imgView.setImage(item.data())

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
            self.noiseMode = confDialog.getSelectedNoiseMode()
            self.noiseParams = confDialog.getSliderValue()
        else:
            pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())
