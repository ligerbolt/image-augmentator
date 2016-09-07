# _*_ coding: utf-8 _*_

import sys
import os.path
import cv2
import glob
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mywidgets import (FileListView, ImageView, PushButton,
        CopyConfigDialog, NoiseConfigDialog, FilterConfigDialog,
        ProgressBarDialog, RotateConfigDialog, HSVConvertConfigDialog)
from constant import Constant
from image import Image
import numpy as np

"""
    メインウインドウクラス（Qwidget継承）
    アプリ画面のUI部品配置・イベントハンドラ定義
"""
class AppWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setModeAndParams()
        self.selectedItem = None

    def initUI(self):

        self.baseLayout = QHBoxLayout()

        """画像ビュワー部定義"""
        self.imgView = ImageView(width=400, height=400)
        self.baseLayout.addWidget(self.imgView)

        """設定ボタン定義"""
        self.sBoxLayout = QGridLayout()
        self.radioGroup = QButtonGroup()
        self.radioBtn1 = QRadioButton("画像コピー")
        self.radioBtn2 = QRadioButton("ノイズ付与")
        self.radioBtn3 = QRadioButton("フィルタリング")
        self.radioBtn4 = QRadioButton("HSV色空間（彩度/明度）補正")
        self.radioBtn5 = QRadioButton("回転")
        self.radioBtn1.setChecked(True)
        self.confBtn1 = PushButton("画像コピー設定", width=150)
        self.confBtn2 = PushButton("ノイズ付与設定", width=150)
        self.confBtn3 = PushButton("フィルタリング設定", width=150)
        self.confBtn4 = PushButton("HSV色空間（彩度/明度）補正設定", width=150)
        self.confBtn5 = PushButton("回転設定", width=150)
        self.confBtn1.clicked.connect(self.__clickedCopyConfButton)
        self.confBtn2.clicked.connect(self.__clickedNoiseConfButton)
        self.confBtn3.clicked.connect(self.__clickedFilterConfButton)
        self.confBtn4.clicked.connect(self.__clickedHSVConvertConfButton)
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

        """画像ファイルリストビュー部定義"""
        self.listView = FileListView()
        self.listView.doubleClicked[QModelIndex].connect(self.__doubleClickedItem)

        """画像フォルダ選択ボタン定義"""
        secLayout = QVBoxLayout()
        secHLayout = QHBoxLayout()
        secLayout.addWidget(QLabel("画像集合格納ディレクトリ"))
        self.txtLine = QLineEdit()
        self.txtLine.setReadOnly(True)
        self.txtLine.setFixedWidth(300)
        self.secButton = QPushButton('Select')
        self.secButton.setFixedWidth(80)
        self.secButton.clicked.connect(self.__clickedSelectButton)
        secHLayout.addWidget(self.txtLine)
        secHLayout.addWidget(self.secButton)
        secLayout.addLayout(secHLayout)
        secLayout.addWidget(self.selectGBox)
        secLayout.addWidget(self.listView)

        """画像複製実行ボタン定義"""
        self.runBtn = PushButton("画像生成", width=400)
        self.runBtn.clicked.connect(self.__clickedRunButton)
        self.runBtn.setEnabled(False)
        secLayout.addWidget(self.runBtn)

        """レイアウトにwidget追加"""
        self.baseLayout.addLayout(secLayout)
        """self.baseLayout.addLayout(self.vlayout)"""
        self.setLayout(self.baseLayout)

        """メインウィンドウ設定・表示"""
        self.setWindowTitle('Image Augmentator')
        self.show()

    """
        画像処理パラメータ初期化メソッド
        画像処理のパラメータ格納辞書を生成
    """
    def setModeAndParams(self):
        self.copyMode = Constant.LR_REVERSAL_MODE
        self.noiseMode = Constant.SOLT_NOISE_MODE
        self.filterMode = Constant.AVERAGE_FILTER_MODE
        self.noiseParams = {"amount": 0.0, "sigma": 0.0}
        self.filterParams = {"ksize": 2, "sigma": 0}
        self.hsvConvParams = {"chroma": 1.0, "value": 1.0}
        self.rotateParams = {"angle": 0.0, "scale": 1.0}

    """
        画像フォルダ選択処理メソッド
        処理対象となる画像群格納フォルダを選択・画像をリストビューに表示
    """
    def __clickedSelectButton(self):
        self.directoryPath = QFileDialog.getExistingDirectory(self,
                '対象画像が入ったフォルダを指定してください', os.path.expanduser('~'))
        self.txtLine.setText(self.directoryPath)
        self.imageFiles = self.listView.addFiles(glob.glob(self.directoryPath + "/*"))
        if len(self.imageFiles) != 0:
            self.runBtn.setEnabled(True)
        else:
            self.runBtn.setEnabled(False)
        self.imgView.clear()
        self.selectedItem = None

    """
        リスト項目選択処理メソッド
        選択画像に画像処理を施し、プレビュー表示する
    """
    def __doubleClickedItem(self, item):
        if self.radioBtn1.isChecked():
            self.image = Image.reversal(item.data(), self.copyMode)
        elif self.radioBtn2.isChecked():
            self.image = Image.addNoise(item.data(),
                                    self.noiseMode, self.noiseParams)
        elif self.radioBtn3.isChecked():
            self.image = Image.filtering(item.data(),
                                    self.filterMode, self.filterParams)
        elif self.radioBtn4.isChecked():
            self.image = Image.multiplyHSVPixels(item.data(), self.hsvConvParams)
        elif self.radioBtn5.isChecked():
            self.image = Image.rotate(item.data(), self.rotateParams)
        else:
            pass

        self.imgView.setCvImage(self.image)
        self.selectedItem = item

    """
        コピー処理設定メソッド
        コピー処理設定ダイアログの表示・パラメータ格納
    """
    def __clickedCopyConfButton(self):
        confDialog = CopyConfigDialog(mode=self.copyMode)
        if confDialog.exec_() == QDialog.Accepted:
            self.copyMode = confDialog.getSelectedCopyMode()
            if not self.selectedItem is None:
                self.__doubleClickedItem(self.selectedItem)
        else:
            pass

    """
        ノイズ付加処理設定メソッド
        ノイズ付加処理設定ダイアログの表示・パラメータ格納
    """
    def __clickedNoiseConfButton(self):
        confDialog = NoiseConfigDialog(mode=self.noiseMode,
                                            params=self.noiseParams)
        if confDialog.exec_() == QDialog.Accepted:
            self.noiseMode, self.noiseParams = confDialog.getSelectedNoiseConfig()
            if not self.selectedItem is None:
                self.__doubleClickedItem(self.selectedItem)
        else:
            pass

    """
        フィルタリング処理設定メソッド
        フィルタリング処理設定ダイアログの表示・パラメータ格納
    """
    def __clickedFilterConfButton(self):
        confDialog = FilterConfigDialog(mode=self.filterMode,
                                            params=self.filterParams)
        if confDialog.exec_() == QDialog.Accepted:
            self.filterMode, self.filterParams = confDialog.getSelectedFilterConfig()
            if not self.selectedItem is None:
                self.__doubleClickedItem(self.selectedItem)

    """
        色空間変換処理設定処理メソッド
        色空間処理設定ダイアログの表示・パラメータ格納
    """
    def __clickedHSVConvertConfButton(self):
        confDialog = HSVConvertConfigDialog(params=self.hsvConvParams)
        if confDialog.exec_() == QDialog.Accepted:
            self.hsvConvParams = confDialog.getSelectedHSVConvConfig()
            if not self.selectedItem is None:
                self.__doubleClickedItem(self.selectedItem)

    """
        回転処理設定処理メソッド
        回転処理設定ダイアログの表示・パラメータ格納
    """
    def __clickedRotateConfButton(self):
        confDialog = RotateConfigDialog(params=self.rotateParams)
        if confDialog.exec_() == QDialog.Accepted:
            self.rotateParams = confDialog.getSelectedRotateConfig()
            if not self.selectedItem is None:
                self.__doubleClickedItem(self.selectedItem)

    """
        画像処理実行処理メソッド
        選択した画像・設定情報を元に画像処理実行・複製
    """
    def __clickedRunButton(self):
        self.setEnabled(False)
        for file in self.imageFiles:
            if self.radioBtn1.isChecked():
                image = Image.reversal(file, self.copyMode)
            elif self.radioBtn2.isChecked():
                image = Image.addNoise(file,
                                    self.noiseMode, self.noiseParams)
            elif self.radioBtn3.isChecked():
                image = Image.filtering(file,
                                    self.filterMode, self.filterParams)
            elif self.radioBtn4.isChecked():
                image = Image.multiplyHSVPixels(file, self.hsvConvParams)
            elif self.radioBtn5.isChecked():
                image = Image.rotate(file, self.rotateParams)
            cv2.imwrite(self.__makeNewFileName(file), image)

        QMessageBox.information(None, "処理完了",
                            "画像処理を施した画像複製が完了しました。")
        self.setEnabled(True)


    """
        ファイル名生成メソッド
        複製画像に付与するファイル名を現時刻情報より生成
    """
    def __makeNewFileName(self, fileName):
        baseName = os.path.basename(fileName)
        todaydetail = datetime.datetime.today()
        nowTimeStr = todaydetail.strftime("%Y%m%d-%H%M%S")
        print(self.directoryPath + "/_COPY_" + nowTimeStr + "_" + baseName)
        return self.directoryPath + "/_COPY_" + nowTimeStr + "_" + baseName


"""
    メイン関数
    アプリwidgetを表示
"""
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())
