# Import necessary libaries
import cv2
import numpy as np
# Bước 1: Load ảnh lên và hiển thị ảnh
img = cv2.imread('sample2.jpg')
clone = img.copy()
cv2.imshow("Input image", img)

rois = []
# Bước 2: Chọn một vài pixel thuộc vùng nền
def roi_average(roi):
    return np.average(roi, axis = (0, 1))

def click_and_crop(event, x, y, flags, param):
    global refPt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False 
        cv2.rectangle(img, refPt[0], refPt[1], (0, 0, 255), 2)
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        rois.append(roi.copy())
        cv2.imshow("Input image", img)
    return rois

cv2.setMouseCallback("Input image", click_and_crop)
refPt = []
cropping = False
while True:
    cv2.imshow("Input image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("r"):
        img = clone.copy()
        rois = []
    elif key == ord("c"):
        break

# close all open windows
cv2.destroyAllWindows()

# Bước 3: Tính giá trị màu đại diện

def get_threshold(rois):
    blue = []
    green = []
    red = []
    for roi in rois:
        blue = blue + roi[:, :, 0].flatten().tolist()
        green = green + roi[:, :, 1].flatten().tolist()
        red = red + roi[:, :, 2].flatten().tolist()
    blue = np.array(blue)
    green = np.array(green)
    red = np.array(red)

    mean = np.array([np.mean(blue), np.mean(green), np.mean(red)])

# Bước 4: Tính độ lệch (threshold)
    var = np.array([np.var(blue), np.var(green), np.var(red)])
    offset = np.sqrt(var)

    threshold = []
    threshold.append(mean - 2 * offset)
    threshold.append(mean + 2 * offset)
    return threshold

# Bước 5: Bắt đầu phân đoạn ảnh với
# giá trị màu đại diện và độ lệch

def separate_background(img):
    new_img = img.copy()
    threshold = get_threshold(rois)
    mask = cv2.inRange(new_img, threshold[0], threshold[1])      
    new_img[mask!=0] = np.array([0, 0, 0])  
    return new_img.copy()

new_img = separate_background(img)
cv2.imshow("Output image", new_img)
cv2.waitKey(0)
# Bước 6: Thay vùng nền bằng ảnh bất kỳ

sample = new_img.copy()
background_image = "image-background2.jpg"
background_image = cv2.imread(background_image)
height, width = sample.shape[:2]
background_image = cv2.resize(background_image, (width, height), interpolation = cv2.INTER_CUBIC)
for i in range(width):
    for j in range(height):
        pixel = sample[j, i]
        if np.all(pixel == [0, 0, 0]):
            sample[j, i] = background_image[j, i]

cv2.imwrite("result2.jpg", sample)