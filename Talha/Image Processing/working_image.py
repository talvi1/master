
import cv2 as cv
import glob
import numpy as np
i = 14

for img in glob.glob('indoor/*.jpg'):
    image1 = cv.imread(img)

    mask = np.ones(image1.shape, dtype=np.uint8)
    mask.fill(255)

    roi_corners = np.array([[(300, 1000), (800, 700), (1200, 700), (1600, 1000)]])

    cv.fillPoly(mask, roi_corners, 0)
    masked_image = cv.bitwise_or(image1 ,mask)

    gray_image = cv.cvtColor(masked_image, cv.COLOR_BGR2GRAY)

    blur = np.ones((5,5),np.float32)/25
    ret, thresh = cv.threshold(blur, 50, 255, cv.THRESH_BINARY)
    blurred = cv.filter2D(gray_image, -1, blur)

    edges = cv.Canny(blurred,0,75)
    kernel = np.ones((5,5),np.uint8)
    dilate = cv.dilate(edges,kernel,iterations = 7)

    new_mask = np.ones(dilate.shape, dtype=np.uint8)
    new_mask.fill(255)
    new_corners = np.array([[(300+20, 1000-20), (800+20, 700+20), (1200+20, 700+20), (1600-20, 1000-20)]])

    cv.fillPoly(new_mask, new_corners, 0)
    masked_image = cv.bitwise_or(dilate, new_mask)

    im2, contours, hierarchy = cv.findContours(masked_image,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    hull = []
    for x in range(len(contours)):
        hull.append(cv.convexHull(contours[x], False))
    for i in range(len(contours)):
        color_contours = (0,255,0)
        color = (0, 255, 0)
        #cv.drawContours(image1, contours, i, color_contours, 5, 8, hierarchy)
        cv.drawContours(image1, hull, i, color, 5, 8)
    cv.imwrite(img, image1)

