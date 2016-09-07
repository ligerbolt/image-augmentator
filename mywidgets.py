# _*_ coding: utf-8 _*_

import os.path
import cv2
import numpy as np
from PyQt5.QtWidgets import (QListView, QAbstractItemView, QMessageBox,
        QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
        QDialog, QGridLayout, QGroupBox, QButtonGroup, QDialogButtonBox,
        QRadioButton, QSlider, QLabel, QLineEdit, QProgressBar)
from PyQt5.QtGui import (QStandardItem, QStandardItemModel,
                                QPixmap, QBrush, QColor, QImage)
from PyQt5.QtCore import Qt, QModelIndex, QSize, pyqtSignal
from constant import Constant


"""
    テキストライン部品クラス（QLineEditクラス継承）
"""
class TextLine(QLineEdit):

    def __init__(self, text=None, width=None, readmode=False):
        super().__init__()
        if not text is None: self.setText(text)
        if not width is None: self.setFixedWidth(width)
        self.setReadOnly(readmode)
        self.setAlignment(Qt.AlignRight)


"""
    スライダー部品クラス（QSliderクラス継承）
"""
class HorizontalSlider(QSlider):

    def __init__(self, width=300, height=50):
        super().__init__(Qt.Horizontal)
        self.setFixedSize(width, height)
        self.initValueAndRange()
        self.valueChanged[int].connect(self.changedValue)

    """レンジ幅・初期値セット処理"""
    def initValueAndRange(self, value=0, minimum=0, maximum=100):
        self.setRange(minimum, maximum)
        self.setValue(value)

    def changedValue(self, value):
        pass


"""
    設定ダイアログ部品クラス（QDialogクラス継承）
"""
class ConfigDialog(QDialog):

    def __init__(self):
        super().__init__()

    def initUI(self):
        self.btnBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btnBox.accepted.connect(self.clickedAccept)
        self.btnBox.rejected.connect(self.clickedReject)

    """OKボタン押下時処理"""
    def clickedAccept(self):
        self.accept()

    """キャンセルボタン押下時処理"""
    def clickedReject(self):
        self.reject()


"""
    画像ビューワ部品クラス（QGraphicsViewクラス継承）
"""
class ImageView(QGraphicsView):

    def __init__(self, width=200, height=300):
        super().__init__()
        self.setFixedSize(QSize(width, height))
        self.image = None
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

    """ファイル名より取得した画像表示"""
    def setImage(self, imageName):
        self.setCvImage(cv2.imread(imageName))

    """numpy配列より取得した画像表示"""
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

    """ビューワクリア処理"""
    def clear(self):
        self.scene.clear()


"""
    画像ファイル名リスト部品クラス（QListViewクラス継承）
"""
class FileListView(QListView):

    def __init__(self):
        super().__init__()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    """画像ファイル抽出＆リスト追加処理"""
    def addFiles(self, files):
        itemCount = 0
        imageFiles = []
        self.model = QStandardItemModel()
        for file in files:
            if self.__isImage(file):
                imageFiles.append(file)
                item = QStandardItem(file)
                if itemCount % 2 == 0:
                    item.setBackground(QBrush(QColor(221, 222, 211)))
                self.model.appendRow(QStandardItem(item))
                itemCount += 1
        if itemCount == 0:
            QMessageBox.information(None, "No Image Files!",
                            "指定ディレクトリには画像がありません。")
        self.setModel(self.model)
        return imageFiles

    """画像ファイル選別処理（拡張子より選別）"""
    def __isImage(self, file):
        ext = os.path.splitext(file)[1].lower()
        return ext in [".jpg", ".jpeg", ".png", ".gif"]


"""
    ボタン部品クラス（QPushButtonクラス継承）
"""
class PushButton(QPushButton):

    def __init__(self, text=None, width=100):
        super().__init__()
        self.setText(text)
        self.setFixedWidth(width)


"""
    コピー処理設定ダイアログクラス（ConfigDialogクラス継承）
"""
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

    """コピー設定モードUI反映処理"""
    def setSelectedCopyMode(self, mode):
        if mode == Constant.LR_REVERSAL_MODE or mode is None:
            self.radioButton1.setChecked(True)
        elif mode == Constant.TB_REVERSAL_MODE:
            self.radioButton2.setChecked(True)
        else:
            self.radioButton3.setChecked(True)

    """コピー設定モード取得処理"""
    def getSelectedCopyMode(self):
        if self.radioButton1.isChecked():
            return Constant.LR_REVERSAL_MODE
        elif self.radioButton2.isChecked():
            return Constant.TB_REVERSAL_MODE
        else:
            return Constant.LRTB_REVERSAL_MODE


"""
    コピー処理設定ダイアログクラス（ConfigDialogクラス継承）
"""
class NoiseConfigDialog(ConfigDialog):

    def __init__(self, mode=None, params=None):
        super().__init__()
        self.initUI()
        self.setSelectedNoiseMode(mode)
        self.soltSlider.initValueAndRange(value=params["amount"])
        self.gaussSlider.initValueAndRange(value=params["sigma"])

    def initUI(self):
        super().initUI()
        self.setWindowTitle("ノイズ付与設定")
        self.layout = QGridLayout()
        self.radioButton1 = QRadioButton("ごま塩ノイズ")
        self.radioButton2 = QRadioButton("gaussianノイズ")
        self.soltSlider = HorizontalSlider()
        self.soltSlider.setTickPosition(QSlider.TicksBelow)
        self.soltSlider.setTickInterval(20)
        self.gaussSlider = HorizontalSlider()
        self.soltTextLine = TextLine(text=str(self.soltSlider.value()),
                                                width=60, readmode=True)
        self.gaussTextLine = TextLine(text=str(self.gaussSlider.value()),
                                                width=60, readmode=True)
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.radioButton1)
        self.buttonGroup.addButton(self.radioButton2)
        self.soltSlider.valueChanged[int].connect(self.changedSoltSliderValue)
        self.gaussSlider.valueChanged[int].connect(self.changedGaussSliderValue)
        self.layout.addWidget(self.radioButton1, 0, 0)
        self.layout.addWidget(QLabel("ノイズ割合"), 1, 0)
        self.layout.addWidget(self.soltSlider, 1, 1)
        self.layout.addWidget(self.soltTextLine, 1, 2)
        self.layout.addWidget(self.radioButton2, 2, 0)
        self.layout.addWidget(QLabel("分散"), 3, 0)
        self.layout.addWidget(self.gaussSlider, 3, 1)
        self.layout.addWidget(self.gaussTextLine, 3, 2)
        self.layout.addWidget(self.btnBox, 4, 2)
        self.setLayout(self.layout)

    """ノイズ処理設定モードUI反映処理"""
    def setSelectedNoiseMode(self, mode):
        if mode == Constant.SOLT_NOISE_MODE or mode is None:
            self.radioButton1.setChecked(True)
        else:
            self.radioButton2.setChecked(True)

    """ノイズ処理設定モード取得処理"""
    def getSelectedNoiseMode(self):
        if self.radioButton1.isChecked():
            return Constant.SOLT_NOISE_MODE
        else:
            return Constant.GAUSSIAN_NOISE_MODE

    """ノイズ設定パラメータ取得処理"""
    def getSelectedNoiseConfig(self):
        noiseParams = {"amount": self.soltSlider.value(),
                        "sigma": self.gaussSlider.value()}
        return self.getSelectedNoiseMode(), noiseParams

    """スライダー値変更反映処理"""
    def changedSoltSliderValue(self, value):
        value = round((value / 100.0) * 5, 2) + 1
        self.soltTextLine.setText(str(value))

    def changedGaussSliderValue(self, value):
        self.gaussTextLine.setText(str(value))


"""
    フィルタリング処理設定ダイアログクラス（ConfigDialogクラス継承）
"""
class FilterConfigDialog(ConfigDialog):

    def __init__(self, mode=None, params=None):
        super().__init__()
        self.initUI()
        self.setSelectedFilterMode(mode)
        self.kSizeSlider.initValueAndRange(minimum=2, maximum=20, value=params["ksize"])
        self.sigmaSlider.initValueAndRange(value=params["sigma"])

    def initUI(self):
        super().initUI()
        self.setWindowTitle("フィルタリング（ぼかし）設定")
        self.layout = QGridLayout()
        self.gaussBtn = QRadioButton("Gaussianフィルタ")
        self.aveBtn = QRadioButton("移動平均フィルタ")
        self.kSizeSlider = HorizontalSlider()
        self.sigmaSlider = HorizontalSlider()
        self.kSizeTextLine = TextLine(text=str(self.kSizeSlider.value()),
                                                    width=50, readmode=True)
        self.sigmaTextLine = TextLine(text=str(self.sigmaSlider.value()),
                                                    width=50, readmode=True)
        self.kSizeSlider.valueChanged[int].connect(self.changedKSizeSliderValue)
        self.sigmaSlider.valueChanged[int].connect(self.changedSigmaSliderValue)
        self.layout.addWidget(self.gaussBtn, 0, 0)
        self.layout.addWidget(self.aveBtn, 0, 1)
        self.layout.addWidget(QLabel("フィルタサイズ"), 1, 0, Qt.AlignCenter)
        self.layout.addWidget(self.kSizeSlider, 1, 1, 1, 2)
        self.layout.addWidget(self.kSizeTextLine, 1, 4)
        self.layout.addWidget(QLabel("分散"), 2, 0, Qt.AlignCenter)
        self.layout.addWidget(self.sigmaSlider, 2, 1, 1, 2)
        self.layout.addWidget(self.sigmaTextLine, 2, 4)
        self.layout.addWidget(self.btnBox, 4, 4)
        self.setLayout(self.layout)

    """フィルタリング設定モードUI反映処理"""
    def setSelectedFilterMode(self, mode):
        if mode == Constant.GAUSSIAN_FILTER_MODE or mode is None:
            self.gaussBtn.setChecked(True)
        else:
            self.aveBtn.setChecked(True)

    """フィルタリング設定モード取得処理"""
    def getSelectedFilterMode(self):
        if self.gaussBtn.isChecked():
            return Constant.GAUSSIAN_FILTER_MODE
        else:
            return Constant.AVERAGE_FILTER_MODE

    """フィルタリング設定パラメータ値取得処理"""
    def getSelectedFilterConfig(self):
        filterParams = {"ksize": self.kSizeSlider.value(),
                        "sigma": self.sigmaSlider.value()}
        return self.getSelectedFilterMode(), filterParams

    """スライダー値変更反映処理"""
    def changedKSizeSliderValue(self, value):
        self.kSizeTextLine.setText(str(value))

    def changedSigmaSliderValue(self, value):
        self.sigmaTextLine.setText(str(value))


"""
    色空間変換処理設定ダイアログクラス（ConfigDialogクラス継承）
"""
class HSVConvertConfigDialog(ConfigDialog):

    def __init__(self, params=None):
        super().__init__()
        self.initUI()
        self.chromaSlider.initValueAndRange(minimum=0, maximum=20, value=params["chroma"]*10)
        self.valueSlider.initValueAndRange(minimum=0, maximum=20, value=params["value"]*10)

    def initUI(self):
        super().initUI()
        self.setWindowTitle("回転設定")
        self.layout = QGridLayout()
        self.chromaSlider = HorizontalSlider()
        self.valueSlider = HorizontalSlider()
        self.chromaTextLine = TextLine(text=str(self.chromaSlider.value()),
                                                    width=50, readmode=True)
        self.valueTextLine = TextLine(text=str(self.valueSlider.value()),
                                                    width=50, readmode=True)
        self.chromaSlider.valueChanged[int].connect(self.changedChromaSliderValue)
        self.valueSlider.valueChanged[int].connect(self.changedValueSliderValue)
        self.layout.addWidget(QLabel("彩度"), 0, 0, Qt.AlignCenter)
        self.layout.addWidget(self.chromaSlider, 0, 1, 1, 2)
        self.layout.addWidget(self.chromaTextLine, 0, 4)
        self.layout.addWidget(QLabel("明度"), 1, 0, Qt.AlignCenter)
        self.layout.addWidget(self.valueSlider, 1, 1, 1, 2)
        self.layout.addWidget(self.valueTextLine, 1, 4)
        self.layout.addWidget(self.btnBox, 2, 4)
        self.setLayout(self.layout)

    """色空間設定パラメータ値取得処理"""
    def getSelectedHSVConvConfig(self):
        hsvConvParams = {"chroma": round(self.chromaSlider.value() * 0.1, 1),
                            "value": round(self.valueSlider.value() * 0.1, 1)}
        return hsvConvParams

    """スライダー値変更反映処理"""
    def changedChromaSliderValue(self, value):
        value = round(value * 0.1, 1)
        self.chromaTextLine.setText(str(value))

    def changedValueSliderValue(self, value):
        value = round(value * 0.1, 1)
        self.valueTextLine.setText(str(value))


"""
    回転処理設定ダイアログクラス（ConfigDialogクラス継承）
"""
class RotateConfigDialog(ConfigDialog):

    def __init__(self, params=None):
        super().__init__()
        self.initUI()
        self.angleSlider.initValueAndRange(minimum=-180, maximum=180, value=params["angle"])
        self.scaleSlider.initValueAndRange(minimum=0, maximum=10, value=params["scale"])

    def initUI(self):
        super().initUI()
        self.setWindowTitle("回転設定")
        self.layout = QGridLayout()
        self.angleSlider = HorizontalSlider()
        self.scaleSlider = HorizontalSlider()
        self.angleTextLine = TextLine(text=str(self.angleSlider.value()),
                                                    width=50, readmode=True)
        self.scaleTextLine = TextLine(text=str(self.scaleSlider.value()),
                                                    width=50, readmode=True)
        self.angleSlider.valueChanged[int].connect(self.changedAngleSliderValue)
        self.scaleSlider.valueChanged[int].connect(self.changedScaleSliderValue)
        self.layout.addWidget(QLabel("回転角度"), 0, 0, Qt.AlignCenter)
        self.layout.addWidget(self.angleSlider, 0, 1, 1, 2)
        self.layout.addWidget(self.angleTextLine, 0, 4)
        self.layout.addWidget(QLabel("ズーム倍率"), 1, 0, Qt.AlignCenter)
        self.layout.addWidget(self.scaleSlider, 1, 1, 1, 2)
        self.layout.addWidget(self.scaleTextLine, 1, 4)
        self.layout.addWidget(self.btnBox, 2, 4)
        self.setLayout(self.layout)

    """回転設定パラメータ値取得処理"""
    def getSelectedRotateConfig(self):
        rotateParams = {"angle": self.angleSlider.value(),
                        "scale": self.scaleSlider.value()}
        return rotateParams

    """スライダー値変更反映処理"""
    def changedAngleSliderValue(self, value):
        self.angleTextLine.setText(str(value))

    def changedScaleSliderValue(self, value):
        self.scaleTextLine.setText(str(value))

