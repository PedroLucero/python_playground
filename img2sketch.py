### By Pedro Lucero, 2022 ###
# So, in some projects I saw myself in the need to show "drawings" or "sketches" 
# of devices and whatnot. I coded this to avoid that. You put in an image and it'll
# apply the canny filter on it, then a bit_not function. 
# It'll look "good enough" to pass as an actual sketch
###
### Hi! I sketch things, just gimme an image with clearly defined lines and tweak the canny thresholds! ###

import cv2 as cv
import numpy as np


def nothing(x): # Needed because of OpenCV reasons
    pass

img_input = input("Enter img (FULL PATH!)\n>>>")
img = cv.imread(img_input)

scale = 80 # Arbitrary default scale 

cv.namedWindow("Trackbar")
cv.createTrackbar("Thresh Hi", "Trackbar", 52, 255, nothing)
cv.createTrackbar("Thresh Lo", "Trackbar", 154, 255, nothing)
cv.createTrackbar("Scale", "Trackbar", scale, 99, nothing)

while True:

    scale = int(cv.getTrackbarPos('Scale', 'Trackbar') + 1)
    cannyHi = int(cv.getTrackbarPos('Thresh Hi', 'Trackbar'))
    cannyLo = int(cv.getTrackbarPos('Thresh Lo', 'Trackbar'))

    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)
    imgNew = cv.resize(img, dim, interpolation=cv.INTER_AREA)


    gray = cv.cvtColor(imgNew, cv.COLOR_BGR2GRAY)
    blurred_mask = cv.GaussianBlur(gray, (3, 3), 0)
    canny = cv.Canny(blurred_mask, cannyLo, cannyHi)
    bit_not = cv.bitwise_not(canny)


    cv.imshow("Drawing", imgNew)
    cv.imshow("Bitnot", bit_not)
    cv.imshow("Blurred", blurred_mask)

    c = cv.waitKey(1)
    if c == 27:
        break
cv.destroyAllWindows()
