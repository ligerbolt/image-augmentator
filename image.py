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
    def addNoise(imgFiles, mode, params):
        img = cv2.imread(imgFiles)
        height, width, channel = img.shape
        if mode == Constant.SOLT_NOISE_MODE:
            amount = params
            noiseImg = img

            salt = np.ceil(amount * img.size * 0.5)
            coords = [np.random.randint(0, i-1 , int(salt))
                                                    for i in img.shape]
            noiseImg[coords[:-1]] = (255, 255, 255)

            pepper = np.ceil(amount* img.size * (1.0 - 0.5))
            coords = [np.random.randint(0, i-1 , int(pepper))
                                                    for i in img.shape]
            noiseImg[coords[:-1]] = (0, 0, 0)
        else:
            mean = 0
            sigma = params
            noises = np.random.normal(mean, sigma, (height, width, channel))
            noises = noises.reshape(height, width, channel).astype(np.int8)
            noiseImg = (img + noises).astype(np.uint8)
        return noiseImg


    @staticmethod
    def filtering(imgFiles, mode, params):
        img = cv2.imread(imgFiles)
        kSize = int(params["ksize"])
        if mode == Constant.GAUSSIAN_FILTER_MODE:
            return cv2.GaussianBlur(img, ksize=(kSize, kSize), sigmaX=params["sigma"])
        else:
            return cv2.blur(img, ksize=(kSize, kSize))


    @staticmethod
    def convertChannelsValue(imgFiles, coefficient, channel=0):
        img = cv2.imread(imgFiles)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img[:,:,channel] = (img[:,:,channel] * coefficient).astype(np.uint8)
        return cv2.cvtColor(img, cv2.COLOR_HSV2BGR).astype(np.uint8)


    @staticmethod
    def rotate(imgFiles, params):
        img = cv2.imread(imgFiles)
        imgSize = tuple([ img.shape[1], img.shape[0] ])
        center = tuple([ int(img.shape[1]/2.), int(img.shape[0]/2.) ])
        rMatrix = cv2.getRotationMatrix2D(center, params["angle"], params["scale"])
        return cv2.warpAffine(img, rMatrix, imgSize, flags=cv2.INTER_CUBIC)

