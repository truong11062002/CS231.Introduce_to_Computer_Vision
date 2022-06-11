import cv2
from cv2 import threshold
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread("input.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

H, W = img.shape[:2]

# Number of black pixel
number_of_black_pix = np.sum(img == 255)

window_name = "Output"

# Thresholding on image

_, thresh = cv2.threshold(img, 225, 255, cv2.THRESH_BINARY_INV)
#cv2.imshow("Thresh", thresh)

kernel = np.ones((5,5), np.uint8)

# Using dilation to removing black distortion


#cv2.imshow("Dilation", dilation)
erosion = cv2.erode(thresh, kernel, cv2.BORDER_REFLECT,iterations=5)

dilation = cv2.dilate(erosion, kernel, iterations=2)
#cv2.imshow("Erosion", erosion)
# Finding contours shape

contours, hierarchy = cv2.findContours(
    dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgb, contours, -1, (0, 255, 0), 2)
cv2.imshow("Draw Contours: ", rgb)
# Getting number of contours

objects = str(len(contours))
# Print number of objects on a image

text = "Number of objects: " + str(objects)
cv2.putText(dilation, text, (10,25), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0,255,255), 1)

# Show result
cv2.imshow("Original", img)
cv2.imshow(window_name, dilation)

# Count number of hemoglobin
print("Number of hemoglobin / Area of Picture: ", number_of_black_pix, "/", H*W)
print("Number of Object: ", objects)
# Save result
filename = "Output.png"
cv2.imwrite(filename, dilation)
cv2.waitKey(0)
cv2.destroyAllWindows