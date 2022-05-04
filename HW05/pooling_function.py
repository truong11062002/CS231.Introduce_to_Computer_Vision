import cv2
import numpy as np

# Load ảnh

img = cv2.imread("kaka.jpg", 0)

# Hiện thị ảnh

cv2.imshow("Image: ", img)
cv2.waitKey(0)

# Xây dựng các hàm maxPooling, avgPooling, medianPooling


"""
    img: ...
    kernel_size: ...


"""
def maxPooling(img, kernel_size=2):
    H = img.shape[0]
    W = img.shape[1]

    output = np.zeros(shape=(H - kernel_size + 1, W - kernel_size + 1))
    for i in range(0, H - kernel_size + 1):
        for j in range(0, W - kernel_size + 1):
            for k in range(0, kernel_size):
                for h in range(0, kernel_size):
                    if output[i][j] < img[i+k][j+h]:
                        output[i][j] = img[i+h][j+k]

    return output

def avgPooling(img, kernel_size=2):
    H = img.shape[0]
    W = img.shape[1]

    output = np.zeros(shape=(H - kernel_size + 1, W - kernel_size + 1))

    for i in range(0 , H - kernel_size + 1):
        for j in range(0, W - kernel_size + 1):
            s = 0
            for k in range(0, kernel_size):
                for h in range(0, kernel_size):
                    for h in range(0, kernel_size):
                        s += img[i+k][j+h]
                output[i][j] = s / (kernel_size*kernel_size)

    return output 

def medianPooling(img, kernel_size=2):
    H = img.shape[0]
    W = img.shape[1]

    output = np.zeros(shape=(H - kernel_size + 1, W - kernel_size + 1))

    for i in range(0, H - kernel_size + 1):
        for j in range(0, W - kernel_size + 1):
            temp = []
            for k in range(0, kernel_size):
                for h in range(0, kernel_size):
                    temp.append(img[i+k][j+h])
            output[i][j] = np.median(temp)

    return output

# show ảnh sử dụng hàm maxPooling
output_maxPooling = maxPooling(img)
cv2.imshow("Max Pooling", output_maxPooling)
cv2.waitKey(0)

# show ảnh sử dụng hàm avgPooling
output_avgPooling = avgPooling(img)
cv2.imshow("Average Pooling", output_avgPooling)
cv2.waitKey(0)

# show ảnh sử dụng hàm medianPooling
output_medianPooling = medianPooling(img)
cv2.imshow("Median Pooling", output_medianPooling)
cv2.waitKey(0)