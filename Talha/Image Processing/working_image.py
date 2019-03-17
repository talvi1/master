
import cv2 as cv
import numpy as np
i = 14

image1 = cv.imread('Images/pothole' + str(i) + '.jpg', -1)

mask = np.ones(image1.shape, dtype=np.uint8)
mask.fill(255)

roi_corners = np.array([[(300, 2400), (1000, 1200), (2400, 1200), (3600, 2400)]])

cv.fillPoly(mask, roi_corners, 0)
cv.imwrite('image_masked.png', mask)
masked_image = cv.bitwise_or(image1 ,mask)

cv.imwrite('new_masked_image.jpg', masked_image)

gray_image = cv.cvtColor(masked_image, cv.COLOR_BGR2GRAY)
#
blur = np.ones((5,5),np.float32)/25
ret, thresh = cv.threshold(blur, 50, 255, cv.THRESH_BINARY)
blurred = cv.filter2D(gray_image, -1, blur)
#
edges = cv.Canny(blurred,0,75)
kernel = np.ones((5,5),np.uint8)
dilate = cv.dilate(edges,kernel,iterations = 7)
roi_corners = np.array([[(300+75, 2400-75), (1000+75, 1200+75), (2400+75, 1200+75), (3600-75, 2400-75)]])
mask = np.ones(dilate.shape, dtype=np.uint8)

print(mask)


cv.fillPoly(mask, roi_corners, 0)
cv.imwrite('image_masked.png', mask)
masked_image = cv.bitwise_or(dilate, mask)




cv.imwrite('image.jpg', masked_image)
cv.imwrite('dilate' + str(i) + '.jpg', dilate)

im2, contours, hierarchy = cv.findContours(masked_image,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
hull = []
for x in range(len(contours)):
    hull.append(cv.convexHull(contours[x], False))
cv.imwrite('contour' + str(i) + '.jpg', im2)
print(thresh.shape[1])
drawing = np.zeros((3024, 4032, 3), np.uint8)
for i in range(len(contours)):
    color_contours = (0,255,0)
    color = (0, 255, 0)
    cv.drawContours(image1, contours, i, color_contours, 5, 8, hierarchy)
    #cv.drawContours(image1, hull, i, color, 5, 8)
cv.imwrite('che' + str(i) + '.jpg', image1)
# cnt = contours[0]
# area = cv.contourArea(cnt)
# print (area)
