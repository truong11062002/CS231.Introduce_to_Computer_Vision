#from select import KQ_NOTE_RENAME
import cv2
import numpy as np
# B1: Load anh
I = cv2.imread("thaotam.jpeg", 0)

# B2: Hien thi anh
# cv2.imshow("Meme", I)
# cv2.waitKey(0)

# B3: Filter anh
filter1 = np.array(
    [[1, 0, -1],
    [1, 0, -1],
    [1, 0, -1]])
filter2 = np.array(
    [[1, 0, -1],
    [2, 0, -2],
    [1, 0, -1]])

filter3 = np.array(
    [[1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1]]
)

filter4 = np.array(
    [[-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]]
)

def max_pooling(I, kernel_size=2):
    H = I.shape[0]
    W = I.shape[1]
    result = np.zeros(shape=(H-kernel_size+1, W-kernel_size+1))
    for hi in range(0, H-kernel_size+1):
        for wi in range(0, W-kernel_size+1):
            for kh in range(0, kernel_size):
                for kw in range(0, kernel_size):
                    if result[hi][wi] < I[hi+kh][wi+kw]:
                        result[hi][wi] = I[hi+kh][wi+kw]
    return result

def avg_pooling(I, kernel_size=2):
    H = I.shape[0]
    W = I.shape[1]
    result = np.zeros(shape=(H-kernel_size+1, W-kernel_size+1))
    for hi in range(0, H-kernel_size+1):
        for wi in range(0, W-kernel_size+1):
            sum = 0
            for kh in range(0, kernel_size):
                for kw in range(0, kernel_size):
                    # print(I[hi+kh][wi+kw])
                    sum += I[hi+kh][wi+kw]
            # print("--------------------------")        
            result[hi][wi] = sum/(kernel_size*kernel_size)
            # print(sum/(kernel_size*kernel_size))
    return result

def median_pooling(I, kernel_size=2):
    H = I.shape[0]
    W = I.shape[1]
    result = np.zeros(shape=(H-kernel_size+1, W-kernel_size+1))
    for hi in range(0, H-kernel_size+1):
        for wi in range(0, W-kernel_size+1):
            kernel_list = []
            for kh in range(0, kernel_size):
                for kw in range(0, kernel_size):
                    kernel_list.append(I[hi+kh][wi+kw])
            result[hi][wi] = np.median(kernel_list)
    return result



def edge_detection(I, filter):
    result1 = cv2.filter2D(I, -1, filter)
    result2 = cv2.filter2D(I, -1, filter.T)
    result3 = cv2.filter2D(I, -1, -filter)
    result4 = cv2.filter2D(I, -1, -filter.T)
    return result1 + result2 + result3 + result4

result1= edge_detection(I, filter1)
result2= edge_detection(I, filter2)

# B4: Hien thi anh sau filter
#cv2.imshow("Hien ho after effect 1", result1)
#cv2.imshow("Hien ho after effect 2", result2)
# cv2.imshow("Hien ho after effect 1", result1)
# cv2.imshow("Hien ho after effect 2", result2)

result_filter1 = cv2.filter2D(I, -1, filter3)
result_filter2 = cv2.filter2D(I, -1, filter4)

cv2.imshow("Anh goc", I)
cv2.imshow("Filter 1", result_filter1)
cv2.imshow("Filter 2", result_filter2)

cv2.waitKey(0)



# max_pooling_visualize = max_pooling(I)
# avg_pooling_visualize = avg_pooling(I)
# med_pooling_visualize = median_pooling(I)

# cv2.imshow("Max pooling visualization", max_pooling_visualize)
# cv2.waitKey(0)

# cv2.imshow("Average pooling visualization", avg_pooling_visualize)
# cv2.waitKey(0)

# cv2.imshow("Median pooling visualization", med_pooling_visualize)
# cv2.waitKey(0)
