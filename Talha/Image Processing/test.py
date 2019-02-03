
import cv2 as cv
import numpy as np
i = 0
while i < 26:
    image1 = cv.imread('Images/pothole' + str(i) + '.jpg')
    gray_image = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)

    blur = np.ones((5,5),np.float32)/25
    blurred = cv.filter2D(gray_image, -1, blur)

    edges = cv.Canny(blurred,0,75)
    kernel = np.ones((5,5),np.uint8)
    dilate = cv.dilate(edges,kernel,iterations = 5)
    cv.imwrite('edges' + str(i) + '.jpg', dilate)
    i += 1
# im2, contours, hierarchy = cv.findContours(img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
# cnt = contours[0]
# area = cv.contourArea(cnt)
# print (area)
