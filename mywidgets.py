# _*_ coding: utf-8 _*_

import os.path
import cv2
import numpy as np
from PyQt5.QtWidgets import (QListView, QAbstractItemView, QMessageBox, QPushButton,
                            QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QDialog,
                            QGridLayout, QGroupBox, QButtonGroup, QDialogButtonBox,
                            QRadioButton, QSlider, QLabel, QLineEdit)
from PyQt5.QtGui import (QStandardItem, QStandardItemModel,
                                QPixmap, QBrush, QColor, QImage)
from PyQt5.QtCore import Qt, QModelIndex, QSize, pyqtSignal
from constant import Constant


class TextLine(QLineEdit):

    def __init__(self, text=None, width=None, readmode=False):
        super().__init__()
        if not text is None: self.setText(text)
        if not width is None: self.setFixedWidth(width)
        self.setReadOnly(readmode)
        self.setAlignment(Qt.AlignRight)


class HorizontalSlider(QSlider):

    def __init__(self, width=300, height=50):
        super().__init__(Qt.Horizontal)
        self.setFixedSize(width, height)
        self.initValueAndRange()
        self.valueChanged[int].connect(self.changedValue)

    def initValueAndRange(self, value=0, minimum=0, maximum=100):
        self.setRange(minimum, maximum)
        self.setValue(value)

    def changedValue(self, value):
        pass


class ConfigDialog(QDialog):

    def __init__(self):
        super().__init__()

    def initUI(self):
        self.btnBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btnBox.accepted.connect(self.clickedAccept)
        self.btnBox.rejected.connect(self.clickedReject)

    def clickedAccept(self):
        self.accept()

    def clickedReject(self):
        self.reject()


class ImageView(QGraphicsView):

    def __init__(self, width=200, height=300):
        super().__init__()
        self.setFixedSize(QSize(width, height))
        self.image = None
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

    def setImage(self, imageName):
        self.setCvImage(cv2.imread(imageName))

    def setCvImage(self, cvImage):
        cvImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        height, width, channel = cvImage.shape
        bytesPerLine = width * channel
        self.image = QImage(cvImage.data, width, height,
                            bytesPerLine, QImage.Format_RGB888)
        item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene = QGraphicsScene()
        self.scene.addItem(item)
        self.setScene(self.scene)

    def clear(self):
        self.scene.clear()


class FileListView(QListView):

    def __init__(self):
        super().__init__()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def addFiles(self, files):
        itemCount = 0
        self.model = QStandardItemModel()
        for file in files:
            if self.__isImage(file):
                item = QStandardItem(file)
                if itemCount % 2 == 0:
                    item.setBackground(QBrush(QColor(221, 222, 211)))
                self.model.appendRow(QStandardItem(item))
                itemCount += 1
        if itemCount == 0:
            QMessageBox.information(None, "No Image Files!",
                            "指定ディレクトリには画像がありません。")
        self.setModel(self.model)

    def __isImage(self, file):
        ext = os.path.splitext(file)[1].lower()
        return ext in [".jpg", ".jpeg", ".png", ".gif"]


class ConfigButton(QPushButton):

    def __init__(self, text=None, width=100):
        super().__init__()
        self.setText(text)
        self.setFixedWidth(width)


class CopyConfigDialog(ConfigDialog):

    def __init__(self, mode=None):
        super().__init__()
        self.__initUI()
        self.setSelectedCopyMode(mode)

    def __initUI(self):
        super().initUI()
        self.setWindowTitle("画像コピー設定")
        self.layout = QGridLayout()
        self.radioGroup = QButtonGroup()
        self.radioButton1 = QRadioButton("左右反転")
        self.radioButton2 = QRadioButton("上下反転")
        self.radioButton3 = QRadioButton("左右上下反転")
        self.radioGroup.addButton(self.radioButton1)
        self.radioGroup.addButton(self.radioButton2)
        self.radioGroup.addButton(self.radioButton3)
        self.layout.addWidget(self.radioButton1, 0, 0)
        self.layout.addWidget(self.radioButton2, 1, 0)
        self.layout.addWidget(self.radioButton3, 2, 0)
        self.layout.addWidget(self.btnBox, 3, 1)
        self.setLayout(self.layout)

    def setSelectedCopyMode(self, mode):
        if mode == Constant.LR_REVERSAL_MODE or mode is None:
            self.radioButton1.setChecked(True)
        elif mode == Constant.TB_REVERSAL_MODE:
            self.radioButton2.setChecked(True)
        else:
            self.radioButton3.setChecked(True)

    def getSelectedCopyMode(self):
        if self.radioButton1.isChecked():
            return Constant.LR_REVERSAL_MODE
        elif self.radioButton2.isChecked():
            return Constant.TB_REVERSAL_MODE
        else:
            return Constant.LRTB_REVERSAL_MODE


class NoiseConfigDialog(ConfigDialog):

    SoltNoiseMode = 0
    GaussianNoiseMode = 1

    def __init__(self, mode=None, params=None):
        super().__init__()
        self.initUI()
        self.setSelectedNoiseMode(mode)
        self.soltSlider.initValueAndRange(value=params["amountValue"])
        self.gaussSlider.initValueAndRange(value=params["alphaValue"])

    def initUI(self):
        super().initUI()
        self.setWindowTitle("ノイズ付与設定")
        self.layout = QGridLayout()
        self.radioButton1 = QRadioButton("ごま塩ノイズ")
        self.radioButton2 = QRadioButton("gaussianノイズ")
        self.soltSlider = HorizontalSlider()
        self.gaussSlider = HorizontalSlider()
        self.soltValueLine = TextLine(text=str(self.soltSlider.value()),
                                                width=60, readmode=True)
        self.gaussValueLine = TextLine(text=str(self.gaussSlider.value()),
                                                width=60, readmode=True)
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.radioButton1)
        self.buttonGroup.addButton(self.radioButton2)
        self.soltSlider.valueChanged[int].connect(self.changedSoltSliderValue)
        self.gaussSlider.valueChanged[int].connect(self.changedGaussSliderValue)
        self.layout.addWidget(self.radioButton1, 0, 0)
        self.layout.addWidget(QLabel("ノイズ割合"), 1, 0)
        self.layout.addWidget(self.soltSlider, 1, 1)
        self.layout.addWidget(self.soltValueLine, 1, 2)
        self.layout.addWidget(self.radioButton2, 2, 0)
        self.layout.addWidget(QLabel("分散"), 3, 0)
        self.layout.addWidget(self.gaussSlider, 3, 1)
        self.layout.addWidget(self.gaussValueLine, 3, 2)
        self.layout.addWidget(self.btnBox, 4, 2)
        self.setLayout(self.layout)

    def setSelectedNoiseMode(self, mode):
        if mode == self.SoltNoiseMode or mode is None:
            self.radioButton1.setChecked(True)
        else:
            self.radioButton2.setChecked(True)

    def getSelectedNoiseMode(self):
        if self.radioButton1.isChecked():
            return self.SoltNoiseMode
        else:
            return self.GaussianNoiseMode

    def getSelectedNoiseConfig(self):
        noiseParams = {"amountValue": self.soltSlider.value(),
                        "alphaValue": self.gaussSlider.value()}
        if self.getSelectedNoiseMode() == Constant.SOLT_NOISE_MODE:
            return self.SoltNoiseMode, noiseParams
        else:
            return self.GaussianNoiseMode, noiseParams

    def changedSoltSliderValue(self, value):
        self.soltValueLine.setText(str(value))

    def changedGaussSliderValue(self, value):
        self.gaussValueLine.setText(str(value))


