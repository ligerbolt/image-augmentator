import cv2
import numpy as np

def flatten_matrix(matrix):
    vector = matrix.flatten(1)
    vector = vector.reshape(1, len(vector))
    return vector


def global_contrast_normalize(vector, scale=1.0, subtract_mean=True, use_std=False,
                              sqrt_bias=0.0, min_divisor=1e-8):

    scale = float(scale)
    mean = vector.mean(axis=1)
    if subtract_mean:
        vector = vector - mean[:, np.newaxis]
    else:
        vector = vector.copy()

    if use_std:
        ddof = 1
        if vector.shape[1] == 1:
            ddof = 0
        normalizers = np.sqrt(sqrt_bias + vector.var(axis=1, ddof=ddof)) / scale
    else:
        normalizers = np.sqrt(sqrt_bias + (vector ** 2).sum(axis=1)) / scale

    normalizers[normalizers < min_divisor] = 1.

    vector /= normalizers[:, np.newaxis]
    return vector


def zca_whitening(inputs):
    sigma = np.dot(inputs, inputs.T) / inputs.shape[1] #Correlation matrix
    U,S,V = np.linalg.svd(sigma) #Singular Value Decomposition
    epsilon = 0.001                #Whitening constant, it prevents division by zero
    ZCAMatrix = np.dot(U, np.diag(1.0 / np.sqrt(S + epsilon))) #ZCA Whitening matrix
    ZCAMatrix = np.dot(ZCAMatrix, U.T)
    return np.dot(ZCAMatrix, inputs)


img = cv2.imread("Lenna.png", 0) #openCV

flatten = flatten_matrix(img)
gcn = global_contrast_normalize(flatten, scale=55, sqrt_bias=10, use_std=True)
white_gcn = zca_whitening(gcn)
img_out = white_gcn.reshape(img.shape[0], img.shape[1], img.shape[2], order='F')
cv2.imwrite("zca_white.jpg", img_out)
print(img_out)
