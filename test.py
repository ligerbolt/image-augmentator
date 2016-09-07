import cv2
import numpy as np
from image import Image

img = Image.rotate("Lenna.png", angle=45.0, scale=2.0)
cv2.imwrite("affine.jpg", img)
