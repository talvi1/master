"""
Author: Talha Alvi
Capstone Project 2019
Description: Script is used to process the images using open cv library. A bounding region is created,
the specfied region is converted to gray scale, is then blurred, edge detection algorithm is used to
find the edges in that part of the road. The edges are dilated and then contour detection and convex hull
algorithms are used to outline the detected potholes and cracks. The detected contours are then overlayed
on to the original raw image. 
"""
import cv2 as cv
import glob
import numpy as np
i = 14

for img in glob.glob('*.jpg'):
    image1 = cv.imread(img)

    mask = np.ones(image1.shape, dtype=np.uint8)
    mask.fill(255)

    roi_corners = np.array([[(520, 1000), (700, 800), (1400, 800), (1650, 1000)]])

    cv.fillPoly(mask, roi_corners, 0)
    masked_image = cv.bitwise_or(image1 ,mask)
    cv.imwrite('masked_image.jpg', masked_image)
    gray_image = cv.cvtColor(masked_image, cv.COLOR_BGR2GRAY)
    cv.imwrite('gray_image.jpg', gray_image)
    blur = np.ones((5,5),np.float32)/25
    ret, thresh = cv.threshold(blur, 50, 255, cv.THRESH_BINARY)
    blurred = cv.GaussianBlur(gray_image, (1, 3), 0)
    cv.imwrite('blurred_image.jpg', blurred)
    #blurred = cv.filter2D(gray_image, -1, blur)
  #  cv.imwrite('blurred.jpg', blurred)
    edges = cv.Canny(blurred, 10, 100)

    new_corners = np.array([[(520+10, 1000-10), (700+10, 800+10), (1400-10, 800+10), (1600-10, 1000-10)]])
    new_mask = np.ones(edges.shape, dtype=np.uint8)

    new_mask.fill(255)
    full_mask = new_mask
  #  cv.imwrite('edges_old.jpg', edges)
    cv.fillPoly(new_mask, new_corners, 0)
  #  cv.imwrite('new_mask.jpg', new_mask)
    mask_inv = cv.bitwise_not(new_mask)
    new_edges = cv.bitwise_and(edges, mask_inv)
    cv.imwrite('edges.jpg', new_edges)
  #  cv.imwrite('mask.jpg', mask_inv)

  #  cv.imwrite('edges.jpg', masked_image)
    kernel = np.ones((5,5),np.uint8)
    dilate = cv.dilate(new_edges ,kernel,iterations = 5)
  #  cv.imwrite('dilate.jpg', dilate)
    cv.imwrite('dilated.jpg', dilate)
    im2, contours, hierarchy = cv.findContours(dilate,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    cv.imwrite('contours.jpg', im2)
    hull = []
    for x in range(len(contours)):
        hull.append(cv.convexHull(contours[x], False))
    c
    for i in range(len(contours)):
        color_contours = (0,255,0)
        color = (0, 255, 0)
        #cv.drawContours(image1, contours, i, color_contours, 5, 8, hierarchy)
        cv.drawContours(image1, hull, i, color, 5, 8)
   # cv.imwrite('Processed.jpg', image1)
    cv.imwrite('Processed.jpg', image1)
