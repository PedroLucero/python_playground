import cv2 as cv
import numpy as np


def nothing(x):
    pass


# Bro just add a copy of the pic in the same directory...

img = cv.imread("C://Users//Pedro//Documents//HUBIOS designs//Images//Thermal Cycler//edited.png")

#img_input = input("Enter img (FULL PATH!)\n>>>")
#img = cv.imread(img_input)

scale = 80

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
