import numpy as np
import cv2

img = cv2.imread('101.jpg', 0)
template = cv2.imread('102.jpg', 0)

result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

cv2.imshow("result",result)
cv2.imshow('Image',img)
cv2.waitKey(0)

def correlation(img, mask):
    max_row = img.shape[0] - mask.shape[0] + 1
    max_col = img.shape[1] - mask.shape[1] + 1

    output = np.zeros([max_row, max_col])

    for curr_row in range(0, max_row):
        for curr_col in range(0, max_col):
            for curr_mask_row in range(0, mask.shape[0]):
                for curr_mask_col in range (0, mask.shape[1]):
                    output[curr_row, curr_col] += img[curr_row + curr_mask_row, curr_col + curr_mask_col] * mask[curr_mask_row, curr_mask_col]
    return output

