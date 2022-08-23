import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

imageDirectory = "image"

for filename in os.listdir(imageDirectory):
    img = cv2.imread(imageDirectory + "/" + filename)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
    lower_green1 = np.array([20, 24, 111])
    upper_green1 = np.array([71, 255, 228])

    mask = cv2.inRange(hsv, lower_green1, upper_green1)

    result = cv2.bitwise_and(img, img, mask = mask)

    cv2.imwrite(("newImages/green/" + filename), result)
    cv2.imwrite(("newImages/mask/" + filename), mask)
