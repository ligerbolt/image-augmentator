# _*_ coding: utf-8 _*_

import cv2
import numpy as np
from mywidgets import *
from constant import Constant

class Image:

    @staticmethod
    def reversal(imgFiles, mode=Constant.LR_REVERSAL_MODE):
        img = cv2.imread(imgFiles)
        return cv2.flip(img, mode)

    @staticmethod
    def addNoise(imgFiles, mode, params=None):
        img = cv2.imread(imgFiles)
        height, width, channel = img.shape
        if mode == Constant.SOLT_NOISE_MODE:
            ratio = 0.5
            amount = 0.004
            noiseImg = img

            salt = np.ceil(amount * img.size * ratio)
            coords = [np.random.randint(0, i-1 , int(salt))
                                                    for i in img.shape]
            noiseImg[coords[:-1]] = (255, 255, 255)

            pepper = np.ceil(amount* img.size * (1.0 - ratio))
            coords = [np.random.randint(0, i-1 , int(pepper))
                                                    for i in img.shape]
            noiseImg[coords[:-1]] = (0, 0, 0)
        else:
            mean = 0
            sigma = params
            noises = np.random.normal(mean, sigma, (height, width, channel))
            noises = noises.reshape(height, width, channel).astype(np.int8)
            noiseImg = (img + noises).astype(np.uint8)
            print(noises)
        return noiseImg

